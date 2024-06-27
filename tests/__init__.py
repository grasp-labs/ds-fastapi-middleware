import jwt
import requests


def patch_auth(monkeypatch):
    monkeypatch.setattr(jwt, "get_unverified_header", lambda x: {"alg": "SHA256"})
    monkeypatch.setattr(
        jwt,
        "decode",
        lambda **kwargs: {
            "iss": "https://auth-dev.grasp-daas.com",
            "aud": "https://grasp-daas.com",
            "sub": "hello@grasplabs.no",
            "rsc": "c8c21d27-b777-4c09-8182-b118cab364bd:tenant",
            "ver": "2.0.0",
            "iat": 1615996800,
            "exp": 1616083200,
            "nbf": 1615996800,
            "jti": "c8c21d27-b777-4c09-8182-b118cab364bd",
            "clas": "user",
            "rol": [],
        },
    )


def patch_permission(monkeypatch, status_code=200, groups=["service.cm.admin"]):
    monkeypatch.setattr(
        requests,
        "get",
        lambda url, headers: MockResponse(
            status_code=status_code, content=[{"name": group} for group in groups]
        ),
    )


class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def json(self):
        return self.content
