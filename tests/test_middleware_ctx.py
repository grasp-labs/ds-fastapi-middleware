import uuid

from fastapi import FastAPI
from fastapi.testclient import TestClient

from middleware import ContextMiddleware


app = FastAPI()

app.add_middleware(ContextMiddleware)


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}


client = TestClient(app)


def test_ctx():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    assert response.headers["x-request-id"] is not None
    uuid.UUID(response.headers["x-request-id"])
