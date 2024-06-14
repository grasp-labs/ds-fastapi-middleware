import json
import logging
import uuid
from decimal import Decimal
from typing import Dict

import boto3
from botocore.exceptions import ClientError

from ds_fastapi_middleware.errors import Errors


class DynamoDbHandler(logging.StreamHandler):
    """
    Handler log messages to a Dynamo table and is designed to be used with
    the standard python logging mechanism.
    """

    def __init__(
        self,
        table_name: str,
        auto_create: bool = True,
        level=logging.DEBUG,
        read_capacity: int = 10,
        write_capacity: int = 10,
    ):
        """Init log handler and store the table handle"""
        logging.StreamHandler.__init__(self, level)
        self._auto_create = auto_create
        self._table = self.get_or_create_dynamodb_table(
            table_name,
            auto_create=auto_create,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
        )

    @staticmethod
    def get_or_create_dynamodb_table(
        table_name: str,
        auto_create: bool = True,
        read_capacity: int = 10,
        write_capacity: int = 10,
    ):
        dynamo_db = boto3.resource("dynamodb")
        table = dynamo_db.Table(table_name)

        try:
            table.table_status
            return table
        except ClientError as exc:
            logging.info(f"Dynamodb Table: {table_name} does not exist.")

            if not auto_create:
                # If resource does not exist and auto-create is disabled
                # we are forced to raise an exception
                raise Errors.AuditException(
                    f"Audit table {table_name} does not exist. {exc}",
                )

            key_schema = [{"AttributeName": "id", "KeyType": "HASH"}]
            attr_def = [{"AttributeName": "id", "AttributeType": "S"}]

            table = dynamo_db.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attr_def,
                ProvisionedThroughput={
                    "ReadCapacityUnits": read_capacity,
                    "WriteCapacityUnits": write_capacity,
                },
            )

            table.wait_until_exists()

            return dynamo_db.Table(table_name)

    def emit(self, record):
        """Store the record in the table. Async insert"""
        try:
            attrs = json.loads(json.dumps(record.msg), parse_float=Decimal)
            self._ensure_id(attrs)
            self._table.put_item(Item=attrs)
        except Exception as exc:
            logging.error(f"Unable to save log record: {record.msg}: {exc}")

    @staticmethod
    def _ensure_id(item: Dict):
        """Ensure the id is in the item"""
        return item.get("id", str(uuid.uuid4()))


def init(
    table: str,
    log_level: str = logging.INFO,
    read_capacity: int = 10,
    write_capacity: int = 10,
) -> logging.Logger:
    """
    Initialize logger with DynamoDB handler.

    @param table: DynamoDB audit table name.
    @param read_capacity: Read capacity.
    @param write_capacity: Write capacity.
    @param log_level: Log level.
    @return: Audit logger instance.
    """
    logger = logging.getLogger(table)
    logger.addHandler(
        DynamoDbHandler(
            table_name=table,
            read_capacity=read_capacity,
            write_capacity=write_capacity,
        )
    )
    logger.setLevel(log_level)
    return logger
