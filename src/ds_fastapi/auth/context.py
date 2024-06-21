"""
Contextual information for request processing.
"""

import contextvars
import json
import typing
import uuid


class Context:
    """
    Immutable object to provide context information for request processing.
    """

    def __init__(
        self,
        # Tracing and general attributes
        tracer=None,
        logger=None,
        auth=None,
        request_id: str = None,
        tenant_id: str = None,
        tenant_name: str = None,
        app_injector=None,
        # JWT claims
        iss: str = None,
        sub: str = None,
        aud: typing.List[str] = None,
        exp: float = None,
        nbf: float = None,
        iat: float = None,
        jti: str = None,
        # Custom Claims
        ver: str = None,
        clas: str = None,
        rsc: str = None,
        rol: typing.List[str] = [],
    ):
        self._tracer = tracer
        self._app_injector = app_injector
        self._logger = logger
        self._auth = auth
        self._request_id = request_id
        self._tenant_id = tenant_id
        self._tenant_name = tenant_name
        # JWT claims
        self._iss = iss
        self._sub = sub
        self._aud = aud
        self._exp = exp
        self._nbf = nbf
        self._iat = iat
        self._jti = jti
        # Custom Claims
        self._ver = ver
        self._clas = clas
        self._rsc = rsc
        self._rol = rol

    """
    Contextvar is natively supported in Asyncio, we can take advantage of this
    of easily get the current context.
    """
    __ctx_var = contextvars.ContextVar("__internal_context_var")

    @classmethod
    def current(cls) -> "Context":
        return cls.__ctx_var.get()

    @classmethod
    def clear_current(cls):
        cls.__ctx_var.set(Context())

    def set_current(self):
        Context.__ctx_var.set(self)

    @classmethod
    def set_current_with_value(
        cls,
        tracer=None,
        app_injector=None,
        logger=None,
        auth=None,
        request_id=None,
        tenant_id=None,
        tenant_name=None,
        iss=None,
        sub=None,
        aud=None,
        exp=None,
        nbf=None,
        iat=None,
        jti=None,
        ver=None,
        clas=None,
        rsc=None,
        rol=None,
    ) -> "Context":
        """
        clone the current context with the given values, set the new ctx as
        current and returns it.
        :return:
        """
        current = cls.current()
        new_ctx = current.with_value(
            tracer=tracer,
            app_injector=app_injector,
            logger=logger,
            auth=auth,
            request_id=request_id,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            iss=iss,
            sub=sub,
            aud=aud,
            exp=exp,
            nbf=nbf,
            iat=iat,
            jti=jti,
            ver=ver,
            clas=clas,
            rsc=rsc,
            rol=rol,
        )
        new_ctx.set_current()
        return new_ctx

    def get(self, key, default=None):
        if hasattr(self, "_" + key):
            return getattr(self, "_" + key)
        return default

    def __getitem__(self, key):
        if hasattr(self, "_" + key):
            return getattr(self, "_" + key)
        raise KeyError(key + " is unknown")

    def __copy__(self):
        return self.__class__(
            logger=self._logger,
            request_id=self._request_id,
            auth=self._auth,
            tenant_id=self._tenant_id,
            tenant_name=self._tenant_name,
            # JWT Claims
            iss=self.iss,
            sub=self.sub,
            aud=self.aud,
            exp=self.exp,
            nbf=self.nbf,
            iat=self.iat,
            jti=self.jti,
            ver=self.ver,
            clas=self.clas,
            rsc=self.rsc,
            rol=self.rol,
        )

    def __dict__(self):
        return {
            "request_id": self._request_id,
            "auth": self._auth,
            "tenant_id": self._tenant_id,
            "tenant_name": self._tenant_name,
            # JWT Claims
            "iss": self.iss,
            "sub": self.sub,
            "aud": self.aud,
            "exp": self.exp,
            "nbf": self.nbf,
            "iat": self.iat,
            "jti": self.jti,
            # Custom Claims
            "ver": self.ver,
            "clas": self.clas,
            "rsc": self.rsc,
            "rol": self.rol,
        }

    def __repr__(self):
        return json.dumps(self.__dict__())

    def with_value(
        self,
        tracer=None,
        app_injector=None,
        logger=None,
        auth=None,
        request_id=None,
        tenant_id=None,
        tenant_name=None,
        iss=None,
        sub=None,
        aud=None,
        exp=None,
        nbf=None,
        iat=None,
        jti=None,
        ver=None,
        clas=None,
        rsc=None,
        rol=None,
    ) -> "Context":
        """Clone context, adding all keys in future logs."""
        cloned = self.__class__(
            tracer=tracer or self._tracer,
            logger=logger or self._logger,
            app_injector=app_injector or self._app_injector,
            request_id=request_id or self._request_id,
            auth=auth or self._auth,
            tenant_id=tenant_id or self._tenant_id,
            tenant_name=tenant_name or self._tenant_name,
            iss=iss or self._iss,
            sub=sub or self._sub,
            aud=aud or self._aud,
            exp=exp or self._exp,
            nbf=nbf or self._nbf,
            iat=iat or self._iat,
            jti=jti or self._jti,
            ver=ver or self._ver,
            clas=clas or self._clas,
            rsc=rsc or self._rsc,
            rol=rol or self._rol,
        )

        return cloned

    @property
    def tracer(self):
        return self._tracer

    @property
    def logger(self):
        return self._logger

    @property
    def app_injector(self) -> typing.Any:
        return self._app_injector

    @property
    def request_id(self) -> typing.Optional[str]:
        if isinstance(self._request_id, uuid.UUID):
            return str(self._request_id)

        return self._request_id

    @property
    def auth(self):
        return self._auth

    @property
    def tenant_id(self) -> str:
        if isinstance(self._tenant_id, uuid.UUID):
            return str(self._tenant_id)

        return self._tenant_id

    @property
    def tenant_name(self) -> str:
        return self._tenant_name

    @property
    def iss(self) -> str:
        return self._iss

    @property
    def sub(self) -> str:
        return self._sub

    @property
    def aud(self) -> typing.List[str]:
        return self._aud

    @property
    def exp(self) -> float:
        return self._exp

    @property
    def nbf(self) -> float:
        return self._nbf

    @property
    def iat(self) -> float:
        return self._iat

    @property
    def jti(self) -> str:
        return self._jti

    @property
    def ver(self) -> str:
        return self._ver

    @property
    def clas(self) -> str:
        return self._clas

    @property
    def rsc(self) -> str:
        return self._rsc

    @property
    def rol(self) -> typing.List[str]:
        return self._rol


def get_ctx() -> Context:
    return Context.current()


def get_or_create_ctx() -> Context:
    """
    This method aims to be used in middleware, where the order of Context creation is not guaranteed
    :return an empty Context with default values
    """
    try:
        return get_ctx()
    except LookupError:
        ctx = Context()
        ctx.set_current()
    return ctx
