"""
Module for permission management of DaaS service platform services.

Permission module make use of entitlement service to determine if a request has permission
to proceed to service endpoint or be dismissed as 403 -Forbidden.

Entitlement service permits requests to proceed if
- user is authenticated
- user is member of required groups

For more details visit core/entitlement.
"""

import os
from functools import wraps
from typing import Union, List

import requests

from ds_fastapi.auth import Context
from ds_fastapi.errors import WebAppException

# from libs.utils.log import DaasLogger


# LOGGER = DaasLogger.LOGGER


def permission_filter(required_roles: Union[str, List[str]]):
    """
    @summary
    Permission filter decorator used to accept or dismiss http requests
    making use of entitlement service.

    @requires
    Decorate endpoint with accepted role:str or roles:list.

    Define which roles is required for endpoint. The role is equivalent to which entitlement group
    the user must be a member or owner of.

    Example::

        SERVICE_USERS = "service.cm.user"
        SERVICE_ADMINS = "service.cm.admin"

        # Using list of roles:
        @router.post("/endpoint/")
        @permission_filter([SERVICE_ADMINS, SERVICE_USERS])
        async def hello():
            return {"message": "World"}

        # Using single role as string:
        @router.post("/endpoint/")
        @permission_filter(SERVICE_USERS)
        async def world():
            return {"message": "Hello"}

    Expected result of calling decorator with required roles as "SERVICE_ADMINS" require user
    to be member of that service group or raise "Forbidden".
    -----------------------------------------------------------

    @attention: The operation "if not list(set(group_names) & set(roles)):"
    checks if the required groups is found in the unique groups the user belong to
    or raise WebAppException, i.e. Forbidden 403.

    @param required_roles: Role as string or list of strings.
    @return: True.
    """
    roles = []
    if isinstance(required_roles, List):
        roles = required_roles
    else:
        roles.append(required_roles)

    def has_permission(func):
        @wraps(func)
        async def wrapper(context: Context, **kwargs):

            if len(roles) <= 0:
                raise WebAppException.create_precondition_failed(
                    message="The endpoint is broken."
                )

            building_mode = os.environ.get("BUILDING_MODE", "dev")
            entitlements_url = (
                "https://grasp-daas.com/api/entitlements-dev/v1/groups/"
                if building_mode == "dev"
                else "https://grasp-daas.com/api/entitlements/v1/groups/"
            )

            headers = {
                "Authorization": f"Bearer {context.auth}",
            }

            response = requests.get(entitlements_url, headers=headers)  # nosec B113

            if response.status_code != 200:
                # if response.status_code not in [401, 403]:
                #     LOGGER.error(f"{response.status_code} {response.content}")

                # LOGGER.error("User is not entitled to use service.")
                raise WebAppException.create_unauthorized()

            groups = response.json()

            group_names = [g.get("name") for g in groups]

            if not list(set(group_names) & set(roles)):
                raise WebAppException.create_forbidden()

            return await func(context=context, **kwargs)

        return wrapper

    return has_permission
