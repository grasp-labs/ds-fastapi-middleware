"""
FastAPI middleware to manage the context of the request.
"""

import uuid
from typing import Optional, Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ds_fastapi.utils.dependency_injection import AppInjector
from ds_fastapi.auth.auth import Context


class ContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, injector: Optional[AppInjector] = None):
        super().__init__(app)
        self._app_injector = injector

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Dispatch method to handle the request and response.
        :param request: FastAPI request object.
        :param call_next: Callable function to call the next middleware.
        :return: FastAPI response object.
        """
        request_id = request.headers.get("Request-ID", str(uuid.uuid4()))
        Context.clear_current()

        ctx = Context(
            request_id=request_id,
            app_injector=self._app_injector,
        )

        ctx.set_current()

        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
        finally:
            Context.clear_current()
        return response
