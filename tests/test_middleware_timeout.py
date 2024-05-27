import asyncio

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport
import pytest

from ds_fastapi_middleware import TimeoutMiddleware


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
        try:
            await client.get("/slow")
        except Exception as exc:
            assert exc.__class__.__name__ == "WebAppException"
            assert exc.status_code == 504
            assert "Gateway timeout out at 1" in exc.detail
            assert "Retry-After" in exc._header
            assert "X-Response-Time" in exc._header
