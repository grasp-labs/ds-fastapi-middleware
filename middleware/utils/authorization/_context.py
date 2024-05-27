"""
Contextual information for request processing.
"""
import contextvars
import json
import uuid
from typing import Any, Optional


class Context:
    """
    Immutable object to provide context information for request processing.
    """

    def __init__(
        self,
        tracer=None,
        logger=None,
        auth=None,
        request_id: str = None,
        tenant_id: str = None,
        tenant_name: str = None,
        user: str = None,
        app_id: str = None,
        is_global_admin_user=False,
        is_customer_admin=False,
        app_injector=None,
    ):
        self._tracer = tracer
        self._logger = logger
        self._auth = auth
        self._request_id = request_id
        self._tenant_id = tenant_id
        self._tenant_name = tenant_name
        self._user = user
        self._app_id = app_id
        self._is_global_admin_user = is_global_admin_user
        self._is_customer_admin = is_customer_admin
        self._app_injector = app_injector

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
        logger=None,
        request_id=None,
        auth=None,
        tenant_id=None,
        tenant_name=None,
        user=None,
        app_id=None,
        is_global_admin_user=False,
        is_customer_admin=False,
        app_injector=None,
    ) -> "Context":
        """
        clone the current context with the given values, set the new ctx as
        current and returns it
        :return:
        """
        current = cls.current()
        new_ctx = current.with_value(
            tracer=tracer,
            logger=logger,
            request_id=request_id,
            auth=auth,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            user=user,
            app_id=app_id,
            is_global_admin_user=is_global_admin_user,
            is_customer_admin=is_customer_admin,
            app_injector=app_injector,
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
            user=self._user,
            app=self._app_id,
            is_global_admin_user=self._is_global_admin_user,
            is_customer_admin=self._is_customer_admin,
        )

    def __dict__(self):
        return {
            "request_id": str(self._request_id) if isinstance(self._request_id, uuid.UUID) else self._request_id,
            "tenant_id": str(self._tenant_id) if isinstance(self._tenant_id, uuid.UUID) else self._tenant_id,
            "user_id": self._user,
        }

    def __repr__(self):
        return json.dumps(self.__dict__())

    def with_value(
        self,
        tracer=None,
        logger=None,
        request_id=None,
        auth=None,
        tenant_id=None,
        tenant_name=None,
        user=None,
        app_id=None,
        is_global_admin_user=False,
        is_customer_admin=False,
        app_injector=None,
    ) -> "Context":
        """Clone context, adding all keys in future logs."""
        cloned = self.__class__(
            tracer=tracer or self._tracer,
            logger=logger or self._logger,
            request_id=request_id or self._request_id,
            auth=auth or self._auth,
            tenant_id=tenant_id or self._tenant_id,
            tenant_name=tenant_name or self._tenant_name,
            user=user or self._user,
            app_id=app_id or self._app_id,
            is_global_admin_user=is_global_admin_user or self._is_global_admin_user,
            is_customer_admin=is_customer_admin or self._is_customer_admin,
            app_injector=app_injector or self._app_injector,
        )

        return cloned

    @property
    def tracer(self):
        return self._tracer

    @property
    def logger(self):
        return self._logger

    @property
    def request_id(self) -> Optional[str]:
        return self._request_id

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def tenant_name(self) -> str:
        return self._tenant_name

    @property
    def auth(self):
        return self._auth

    @property
    def user(self) -> Optional[str]:
        return self._user

    @property
    def app_id(self) -> Optional[str]:
        return self._app_id

    @property
    def is_global_admin_user(self) -> bool:
        return self._is_global_admin_user

    @property
    def is_customer_admin(self) -> bool:
        return self._is_customer_admin

    @property
    def app_injector(self) -> Any:
        return self._app_injector


def get_ctx() -> Context:
    return Context.current()


def get_or_create_ctx() -> Context:
    """
    This method aims to be used in middleware, where the order of Context
    creation is not guaranteed
    :return an empty Context with default values
    """
    try:
        return get_ctx()
    except LookupError:
        ctx = Context()
        ctx.set_current()
    return ctx
