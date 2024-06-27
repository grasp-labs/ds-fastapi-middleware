import os

import boto3
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from moto import mock_aws

from ds_fastapi.auth import Authentication, get_ctx, Context
from ds_fastapi.middlewares import AuditMiddleware, ContextMiddleware
from ds_fastapi.utils.log.audit import init
from tests import patch_auth


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

    require_auth = Authentication(
        jwt_key="jwt_key",
    )

    # Add middleware
    app.add_middleware(AuditMiddleware, logger=logger, networks=["192.168.0.0/16"])
    app.add_middleware(ContextMiddleware)

    @app.get("/hello")
    async def hello():
        return {"message": "Hello World"}

    @app.get("/forbidden", dependencies=[Depends(require_auth)])
    async def forbidden(
        context: Context = Depends(get_ctx),
    ):
        return context.current().__dict__()

    client = TestClient(app)
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.headers["x-audit-id"] is not None
    assert response.headers["x-process-time"] is not None
    assert response.headers["x-audit-id"] == "N/A"

    # Test endpoint with authentication
    patch_auth(monkeypatch)
    monkeypatch.setattr(AuditMiddleware, "_get_ip", lambda x, y: "10.0.0.234")
    response = client.get("/forbidden", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    assert response.headers["x-audit-id"] != "N/A"
    record = dynamodb.Table(table_name).get_item(
        Key={"id": response.headers["x-audit-id"]}
    )
    assert record is not None
