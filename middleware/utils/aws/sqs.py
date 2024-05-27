import typing

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from middleware.errors import _exceptions as Errors
from middleware.utils.aws.client_factory import BotoClientFactory


def get_sqs_url_by_name(queue_name: str) -> str:
    client = BotoClientFactory.get_boto_client(client_type="sqs")
    response = client.get_queue_url(
        QueueName=queue_name,
    )
    return response.get("QueueUrl")


def dict_to_message_attributes(data: typing.Dict) -> typing.Dict:
    """
    Convert dict to SQS message attributes.
    """
    message_attributes = {}
    for key, value in data.items():
        entry = {}
        if not value:
            continue

        elif isinstance(value, str):
            entry["DataType"] = "String"
            entry["StringValue"] = value
        elif isinstance(value, int):
            entry["DataType"] = "Number"
            entry["StringValue"] = str(value)
        elif isinstance(value, float):
            entry["DataType"] = "Number"
            entry["StringValue"] = str(value)
        elif isinstance(value, bytes):
            entry["DataType"] = "Binary"
            entry["BinaryValue"] = value
        elif isinstance(value, list):
            entry["DataType"] = "String.Array"
            entry["StringValue"] = ",".join(str(item) for item in value)
        # Add more type checks as needed...
        else:
            # Handle unsupported data types
            raise Errors.ValueErrorException(
                f"Unsupported data type for attribute value: {type(value)}"
            )

        message_attributes[key] = entry

    return message_attributes


def publish_message(
    client: BaseClient = None,
    queue_name: str = None,
    queue_url: str = None,
    message: typing.Dict = None,
    body: str = None,
    delay_time: int = 0,
    message_group_id: str = None,
    message_deduplication_id: str = None,
) -> str:
    """
    Publishes a message to an SQS queue.

    If both `queue_url` and `queue_name` are provided, `queue_url` will be used.

    Args:
        client (BaseClient): SQS client.
        queue_name (str): Name of the SQS queue.
        queue_url (str): URL of the SQS queue.
        message (typing.Dict): Message content as a dictionary.
        body (str): Body of the message to send.
        delay_time (int): Delay in seconds before the message becomes visible.
        message_group_id (str): (FIFO) Tag that a message belongs to a specific message group.
        message_deduplication_id (str): (FIFO) Token used for deduplication of messages.

    Returns:
        str: The ID of the published message.

    Raises:
        ValueError: If both `queue_url` and `queue_name` are None.
        ValueError: If required parameters are missing for FIFO queues.
        ClientError: If there's an error publishing the message.

    # Change Log
    ## 2023.05.30:  Allow passing `client` and `queue_url` as arguments to
                    improve performance.
    ## 2023.10.17:  Added requirements to send to FIFO queues.
    """

    if not queue_url and not queue_name:
        raise Errors.ValueErrorException(
            "At least provide one argument: queue_url or queue_name."
        )

    if not client:
        client = BotoClientFactory.get_boto_client(client_type="sqs")

    if not queue_url:
        queue_url = get_sqs_url_by_name(queue_name)

    if not body:
        body = queue_name

    fifo_queue = "fifo" in f"{queue_url}-{queue_name}".lower()

    if fifo_queue and not all([message_group_id, message_deduplication_id]):
        raise Errors.ValueErrorException(
            "Provide 'message_group_id' and 'message_deduplication_id' for FIFO queues."
        )

    message_attrs = dict_to_message_attributes(message)

    try:
        if not message_deduplication_id:
            result = client.send_message(
                QueueUrl=queue_url,
                MessageBody=body,
                MessageAttributes=message_attrs,
                DelaySeconds=delay_time,
            )
            return result.get("MessageId")

        result = client.send_message(
            QueueUrl=queue_url,
            MessageBody=body,
            MessageAttributes=message_attrs,
            DelaySeconds=delay_time,
            MessageGroupId=message_group_id,
            MessageDeduplicationId=message_deduplication_id if fifo_queue else None,
        )
        return result.get("MessageId")

    except ClientError as exc:
        print(f"Failed to publish message: {message}, with exception: {exc}.")
        raise
