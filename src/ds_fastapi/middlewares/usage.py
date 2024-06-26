"""
Usage middleware for tracing service usage in fastApi applications.

Usage metrics is collected and written to storage system for
the purpose of billing customer.

Example::

    from fastapi import FastAPI
    from ds_fastapi.middlewares import UsageMiddleware

    app = FastAPI()
    app.add_middleware(
        UsageMiddleware,
        product_id="product_id",
        memory_mb=1024,
        queue_name="queue_name",
    )
"""

import datetime
import typing
from uuid import UUID

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from ds_fastapi.middlewares import models
from ds_fastapi.utils.usage import write_usage


class UsageMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        product_id: UUID,
        memory_mb: int,
        queue_name: str,
    ):
        """
        Usage middleware for tracing service usage in fastApi applications.

        @param product_id: Product UUID.
        @param memory_mb: Memory in megabytes as integer.
        @param queue_name: Queue name to write the message.
        """
        self.product_id = product_id
        self.memory_mb = memory_mb
        self.queue_name = queue_name
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: typing.Callable):
        """
        Function to collect usage data and write to Cost database.
        @param request: Request object.
        @param call_next: Function to call next.
        @return: Response.
        """
        start_time = datetime.datetime.utcnow()
        response = await call_next(request)
        end_timestamp = datetime.datetime.utcnow()

        if not hasattr(request.state, "context"):
            # Context object does not exist, authorization
            # never happened.
            return response

        ctx = request.state.context
        tenant_id = ctx.tenant_id
        logger = ctx.logger

        usage = models.UsagePayload(
            product_id=self.product_id,
            tenant_id=tenant_id,
            memory_mb=self.memory_mb,
            start_time=start_time,
            end_time=end_timestamp,
            workflow=request.url.path,
        )
        logger.info("Writing usage.")
        write_usage(usage=usage, queue_name=self.queue_name)
        response.headers["X-Usage-Id"] = str(usage.id)
        return response
