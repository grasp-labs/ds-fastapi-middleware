"""
Module for authorization of DaaS service platform services.
"""

import logging
import jwt

from fastapi import Request, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.authentication import AuthCredentials

from context import get_or_create_ctx, Context
from ds_fastapi_middleware.errors import WebAppException
from libs.utils import log_prefix
from libs.utils.log import DaasLogger


class AuthConfig:
    """
    This class configures and enforces user authentication.
    Note that the implementation is tightly coupled
    to the Grasp Identity Server JWT token schema.

    Example::
    >>> config = AuthConfig(
    >>>     jwt_key="jwt_key",
    >>>     iss="https://auth-dev.grasp-daas.com",
    >>> )
    >>> app = FastAPI()
    >>> dependencies = [Depends(config)]
    >>> app.include_router(
    >>>     router=some_router,
    >>>     dependencies=dependencies
    >>> )


    :param jwt_key: The key for the JWT.
    :param oauth_key: The key for the OAuth.
    :param aud: The audience.
    :param iss: The issuer.
    :param token_schema: The token schema.
    """

    def __init__(
        self,
        jwt_key: str,
        iss: str,
        aud: str = ["https://grasp-daas.com"],
        token_schema: str = "Bearer",  # nosec
    ):
        self.TOKEN_SCHEMA = token_schema
        logger.setLevel(logging.WARNING)
        self.aud = aud
        self.iss = iss
        self.jwt_key = jwt_key

    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        """
        Function for authenticating users. Function decode token using encryption key
        of identity server (the token distributor), assert token is valid or raise
        WebAppException (Unauthorized).

        If token is valid and user can be recognized, function proceeds to:
        - Setup logger with tenant/user prefix
        - Define Request context, i.e. assigning user and tenant attributes
        to current Context object.
        """
        token = credentials.credentials
        if not token:
            raise WebAppException.create_unauthorized(message="Missing token.")

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
            )
        except jwt.exceptions.PyJWTError as exc:
            raise WebAppException.create_unauthorized(message=str(exc))

        tenant_id, tenant_name = decoded_token.get("rsc").split(":")
        sub = decoded_token.get("sub")

        logger = DaasLogger()
        logger.setup_logger(prefix=log_prefix(tenant_id=tenant_id, subject_id=sub))

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
