import asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport
import pytest

from ds_fastapi.middlewares import TimeoutMiddleware


app = FastAPI()

app.add_middleware(TimeoutMiddleware, timeout=1)


@app.get("/slow")
async def slow_endpoint():
    await asyncio.sleep(2)
    return {"message": "This endpoint is slow"}


@app.get("/fast")
async def fast_endpoint():
    return {"message": "This endpoint is fast"}


client = TestClient(app)


@pytest.mark.asyncio
async def test_fast_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/fast")
        assert "x-response-time" in response.headers
        assert response.status_code == 200
        assert response.json() == {"message": "This endpoint is fast"}


@pytest.mark.asyncio
async def test_slow_endpoint_timeout():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/slow")
        assert response.status_code == 504
        assert "Gateway timeout at 1" in response.json()["message"]
        assert "Retry-After" in response.headers
        assert "X-Response-Time" in response.headers
