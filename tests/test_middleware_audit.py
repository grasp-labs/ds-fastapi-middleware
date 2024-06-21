import os

import boto3
from fastapi import FastAPI
from fastapi.testclient import TestClient
from moto import mock_aws

from ds_fastapi.middlewares import AuditMiddleware
from ds_fastapi.utils.log.audit import init


@mock_aws()
def test_init(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-north-1")
    assert os.getenv("AWS_DEFAULT_REGION") == "eu-north-1"
    print("Creating table...")
    dynamodb = boto3.resource("dynamodb", region_name="eu-north-1")
    table_name = "unittest-audit"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],  # Partition key
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],  # String
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    # Initialize DynamoDB handler
    logger = init("unittest-audit")

    # Initialize FastAPI app
    app = FastAPI()

    # Add middleware
    app.add_middleware(AuditMiddleware, logger=logger, networks=[])

    @app.get("/hello")
    async def hello():
        return {"message": "Hello World"}

    client = TestClient(app)
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.headers["x-audit-id"] is not None
