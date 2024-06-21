import uuid

import boto3
from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from moto import mock_aws

from ds_fastapi.middlewares import ContextMiddleware, UsageMiddleware
from ds_fastapi.auth.auth import Context, get_or_create_ctx
from ds_fastapi.utils.log.stdout import Logger


def mock_authorize(request: Request):
    _logger = Logger()
    _logger.setup_logger(prefix="[unittest]")
    logger = _logger.LOGGER

    ctx = get_or_create_ctx()

    ctx.set_current_with_value(
        logger=logger,
        tenant_id=uuid.uuid4(),
        tenant_name="test tenant",
        auth="test_auth",
        sub="test_user",
        app_injector="test_app_injector",
    )
    request.state.context = Context.current()


app = FastAPI()


app.add_middleware(
    UsageMiddleware,
    product_id=uuid.uuid4(),
    memory_mb=2048,
    queue_name="default",
)
app.add_middleware(ContextMiddleware)

dependencies = [Depends(mock_authorize, use_cache=False)]


@app.get("/hello")
async def hello(request: Request, _=Depends(mock_authorize)):
    return {"message": "Hello World", "context": request.state.context}


client = TestClient(app)


@mock_aws()
def test_usage():
    sqs = boto3.resource("sqs", region_name="eu-north-1")
    queue_name = "default"
    sqs.create_queue(QueueName=queue_name)
    response = client.get("/hello")
    assert response.status_code == 200
    assert "x-usage-id" in response.headers
    assert response.headers["x-usage-id"] is not None
