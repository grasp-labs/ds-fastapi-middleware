"""Module for service middleware"""

from ds_fastapi_middleware import models

from ds_fastapi_middleware.utils.aws.sqs import publish_message


def write_usage(usage: models.UsagePayload, queue_name: str):
    """
    Function to write usage metrics.
    @param usage: Usage model instance.
    @param queue_name: Queue name to write the message.
    @return: Message ID.
    """

    return publish_message(
        queue_name=queue_name,
        message=usage.jsonable_dict(),
    )
