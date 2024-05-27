"""
FastAPI middleware for keeping revision trail.

The purpose of audit logging is to maintain a revision trail for any requests
that trigger functionality within the system. According to this definition:
-   Unauthorized requests will not trigger functionality and, therefore, will not
    be logged by the audit middleware.
-   Internal traffic that does not trigger functionality will also not be logged.

-   When a user is authenticated, the audit log will record the following
    details:

*   Which user performed the action
*   What action was performed
*   When the action occurred
*   The result of the action

Example:
>>> audit_logger = logging.getLogger("service-name-audit")
>>> audit_logger.addHandler(DynamoDbHandler(table_name="service-name-test"))
>>> audit_logger.setLevel(logging.INFO)
>>> app.add_middleware(AuditMiddleware, logger=audit_logger)


@note
* Dynamodb table will be created if not existing.
* Actions from unauthorized user and internal ips are ignored.
"""
from dataclasses import asdict
import datetime
from typing import Union

from fastapi import FastAPI
import requests
from starlette.middleware.base import BaseHTTPMiddleware

from middleware.models import AuditPayload
from middleware.utils import internal_traffic


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware for creating audit records on all requests made to fastAPI
    web frameworks.

    Middleware secure that on all requests made to api's, internal and
    internet facing, a record will be created on which user, tenant and
    service, how the service was used, from which IP at what time.
    """

    def __init__(self, app: FastAPI, *, logger, **kwargs):
        self._logger = logger
        super().__init__(app)

    async def dispatch(
        self,
        request: requests.Request,
        call_next: callable,
    ) -> requests.Response:
        """
        Dispatch method to handle the request and response.
        :param request: FastAPI request object.
        :param call_next: Callable function to call the next middleware.
        :return: FastAPI response object.
        """
        start_time = datetime.datetime.utcnow().timestamp()
        response = await call_next(request)
        process_time = datetime.datetime.utcnow().timestamp() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        if not self._exclude_traffic(request):
            ctx = request.state.context
            ip = self._get_ip(request)

            audit_item = AuditPayload(
                id=ctx.request_id,
                url=str(request.url),
                method=request.method,
                client_ip=ip,
                status_code=response.status_code,
                tenant_id=ctx.tenant_id,
                user_id=ctx.user,
                created_at= datetime.datetime.fromtimestamp(start_time).isoformat(),
                process_time=str(process_time),
            )
            self._logger.info(asdict(audit_item))
            response.headers["X-Audit-ID"] = ctx.request_id
        else:
            response.headers["X-Audit-ID"] = "N/A"

        return response

    def _exclude_traffic(self, request: requests.Request) -> bool:
        """
        Exclusion of Network Traffic for Usage Logs

        Network traffic generated from services such as Application
        Load Balancers (ALBs) and health checks will be excluded from
        usage logs.

        Be mindful of the following:
        - Intended for services running behind a load balancer.

        :param request: FastAPI request object.
        :return: Bool.
        """
        if not hasattr(request.state, "context"):
            return True

        context = request.state.context
        if not context.tenant_id or not context.user:
            return True

        ip = self._get_ip(request)
        if not ip:
            return True

        if internal_traffic.is_private_ip(ip):
            return True

        return False

    @staticmethod
    def _get_ip(request: requests.Request) -> Union[str, None]:
        """
        Function to get the IP address of the client making the request.
        :param request: FastAPI request object.
        :return: Union[str, None].
        """
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"]
        return None
