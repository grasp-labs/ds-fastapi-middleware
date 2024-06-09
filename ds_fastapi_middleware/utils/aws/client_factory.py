"""
Factory to create boto3 client.
"""
import os

import boto3
from botocore.client import BaseClient
from botocore.config import Config


class BotoClientFactory:
    @staticmethod
    def get_boto_client(client_type: str) -> BaseClient:
        """
        Use session to initiate the connectivity to AWS services.
        See the link for more detail: https://ben11kehoe.medium.com/boto3-sessions-and-why-you-should-use-them-9b094eb5ca8e#:~:text=a%20session%2C%20then%3F-,The%20boto3.,talk%20to%20an%20AWS%20service.
        """
        region = os.environ.get("AWS_DEFAULT_REGION", "eu-north-1")
        session = boto3.session.Session(region_name=region)
        config = Config(
            region_name=region,
            connect_timeout=30,
            retries={"max_attempts": 10, "mode": "standard"},
        )
        return session.client(
            service_name=client_type,
            config=config,
        )
