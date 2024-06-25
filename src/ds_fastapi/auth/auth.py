"""
Module for authorization of DaaS service platform services.
"""

import jwt
import os

from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.authentication import AuthCredentials

from ds_fastapi.auth.context import get_or_create_ctx, Context
from ds_fastapi.errors import WebAppException
from ds_fastapi.utils.log.stdout import Logger


class Authentication:
    """
    Creates a callable object that can be used as a dependecy
    in FastAPI routes to decode authentication headers.

    Example::

        from ds_fastapi import Authentication
        auth = Authentication(
            jwt_key="jwt_key",
        )
        app = FastAPI()

        @app.get("/hello", dependencies=[Depends(auth)])
        async def hello():
            return {"message": "Hello World"}


    :param jwt_key: The public JWT key.
    :param aud: The JWT audience.
    :param iss: The JWT issuer.
    :param token_schema: The token schema.
    :
    """

    ISSUER = (
        "https://auth-dev.grasp-daas.com"
        if os.environ.get("BUILDING_MODE", "dev").lower() != "prod"
        else "https://auth.grasp-daas.com"
    )
    AUDIENCE = ["https://grasp-daas.com"]
    TOKEN_SCHEMA = "Bearer"  # nosec

    def __init__(
        self,
        jwt_key: str = None,
        iss: str = None,
        aud: str = None,
        token_schema: str = None,
        decode_leeway: float = 3,
    ):
        self.jwt_key = jwt_key
        self.TOKEN_SCHEMA = token_schema if token_schema else self.TOKEN_SCHEMA
        self.aud = aud if aud else self.AUDIENCE
        self.iss = iss if iss else self.ISSUER
        self.decode_leeway = decode_leeway

    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False)
        ),
    ):
        """
        Function for authenticating users. Function decode token using encryption key
        of identity server (the token distributor), assert token is valid or raise
        WebAppException (Unauthorized).

        If token is valid and user can be recognized, function proceeds to:
        - Setup logger with tenant/user prefix
        - Define Request context, i.e. assigning user and tenant attributes
        to current Context object.

        Sidenote:
        Reason for passing auto_error=False to HTTPBearer is discussed
        here https://github.com/tiangolo/fastapi/issues/10177
        """
        if not credentials or not credentials.credentials:
            raise WebAppException.create_unauthorized(message="Missing token.")

        token = credentials.credentials

        request.scope["auth"] = AuthCredentials(["authenticated"])

        try:
            jwt_header = jwt.get_unverified_header(token)
            algo = jwt_header.get("alg")
            decoded_token = jwt.decode(
                jwt=token,
                algorithms=[algo],
                audience=self.aud,
                issuer=self.iss,
                key=self.jwt_key,
                leeway=self.decode_leeway,
            )
        except jwt.exceptions.PyJWTError as exc:
            raise WebAppException.create_unauthorized(message=str(exc))

        tenant_id, tenant_name = decoded_token.get("rsc").split(":")
        sub = decoded_token.get("sub")

        logger = Logger()
        logger.setup_logger(prefix=f"[{tenant_id}][{sub}]")

        ctx = get_or_create_ctx()

        ctx.set_current_with_value(
            auth=token,
            logger=logger,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            iss=decoded_token.get("iss"),
            sub=sub,
            aud=decoded_token.get("aud"),
            exp=decoded_token.get("exp"),
            nbf=decoded_token.get("nbf"),
            iat=decoded_token.get("iat"),
            jti=decoded_token.get("jti"),
            ver=decoded_token.get("ver"),
            clas=decoded_token.get("cls"),
            rsc=decoded_token.get("rsc"),
            rol=decoded_token.get("rol"),
        )

        request.state.context = Context.current()
