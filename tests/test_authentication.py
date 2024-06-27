from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient

from ds_fastapi.auth.auth import Authentication
from ds_fastapi.auth.context import get_ctx, Context
from ds_fastapi.auth.perm import permission_filter

from tests import patch_auth, patch_permission


app = FastAPI()

require_auth = Authentication(
    jwt_key="jwt_key",
)


@app.get("/hello", dependencies=[Depends(require_auth)])
async def hello():
    return {"message": "Hello World"}


@app.get("/forbidden", dependencies=[Depends(require_auth)])
@permission_filter("service.cm.admin")
async def forbidden(
    context: Context = Depends(get_ctx),
):
    return {"message": "Forbidden"}


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
    patch_auth(monkeypatch)
    response = client.get("/hello", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "Hello World"}


def test_permission_denied(monkeypatch):
    """
    Verify that the API returns a 403 status code when the user does not have the required permission.
    """
    patch_auth(monkeypatch)
    patch_permission(monkeypatch, groups=[])
    response = client.get("/forbidden", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 403


def test_permission_access_denied(monkeypatch):
    """
    Verify that the API returns a 403 status code when the user does not have the required permission.
    """
    patch_auth(monkeypatch)
    patch_permission(monkeypatch, status_code=403)
    response = client.get("/forbidden", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 401


def test_permission_internal_error(monkeypatch):
    """
    Verify that the API returns a 403 status code when the user does not have the required permission.
    """
    patch_auth(monkeypatch)
    patch_permission(monkeypatch, status_code=500)
    response = client.get("/forbidden", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 401


def test_permission(monkeypatch):
    """
    Verify that the API returns a 200 status code when the user has the required permission.
    """
    patch_auth(monkeypatch)
    patch_permission(monkeypatch)
    response = client.get("/forbidden", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "Forbidden"}
