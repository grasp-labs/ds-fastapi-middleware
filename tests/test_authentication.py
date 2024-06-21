import jwt
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from ds_fastapi.auth.auth import Authentication


app = FastAPI()

require_auth = Authentication(
    jwt_key="jwt_key",
)


@app.get("/hello", dependencies=[Depends(require_auth)])
async def hello():
    return {"message": "Hello World"}


client = TestClient(app)


def test_no_auth_header():
    """
    Verify that the API returns a 401 status code when no auth is provided.


    """
    response = client.get("/hello")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing token."}


def test_invalid_auth_header():
    """
    Verify that the API returns a 401 status code when an invalid auth is provided.
    """
    response = client.get("/hello", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401


def test_valid_auth_header(monkeypatch):
    """
    Verify that the API returns a 200 status code when a valid auth is provided.
    """
    monkeypatch.setattr(jwt, "get_unverified_header", lambda x: {"alg": "SHA256"})
    monkeypatch.setattr(
        jwt,
        "decode",
        lambda **kwargs: {
            "iss": "https://auth-dev.grasp-daas.com",
            "aud": "https://grasp-daas.com",
            "sub": "hello@grasplabs.no",
            "rsc": "c8c21d27-b777-4c09-8182-b118cab364bd:tenant",
        },
    )
    response = client.get("/hello", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "Hello World"}
