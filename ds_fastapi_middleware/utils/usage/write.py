"""Module for service middleware"""

from ds_fastapi_middleware.config import Config
from ds_fastapi_middleware import models

from ds_fastapi_middleware.utils.aws.sqs import publish_message


def write_usage(usage: models.UsagePayload):
    """
    Function to write usage metrics.
    @param usage: Usage model instance.
    @return: Message ID.
    """
    queue_name = Config["aws"]["sqs"]["name"]

    return publish_message(
        queue_name=queue_name,
        message=usage.jsonable_dict(),
    )