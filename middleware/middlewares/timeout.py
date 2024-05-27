import asyncio
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from middleware.errors import WebAppException


class TimeoutMiddleware(BaseHTTPMiddleware):
    """
    Returning a 504 error if the request processing time is above a
    certain threshold.
    """

    def __init__(
        self,
        app: FastAPI,
        *,
        timeout: int = 30,
        retry_after: int = 1,
        **_,
    ) -> None:
        self._timeout = timeout
        self._retry_after = retry_after
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            start_time = time.time()
            response = await asyncio.wait_for(
                call_next(request),
                timeout=self._timeout,
            )
            duration = time.time() - start_time
            response.headers['X-Response-Time'] = str(duration)
            return response

        except asyncio.TimeoutError:
            process_time = time.time() - start_time
            raise WebAppException.create_gateway_timeout(
                message=f"Gateway timeout out at {process_time} seconds.",
                header={
                    "Retry-After": str(self._retry_after),
                    "X-Response-Time": f"{process_time} seconds.",
                },
            )
