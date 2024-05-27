"""
Web application exceptions.
"""

from http import HTTPStatus
from fastapi import HTTPException
import typing


class WebAppException(HTTPException):
    def __init__(
        self,
        status: int,
        reason: str,
        message: str,
        debugging_info: str = None,
        errors: typing.Optional[typing.List[str]] = None,
        header: typing.Optional[typing.Dict[str, str]] = None,
    ):
        self._status = status
        self._reason = reason
        self._message = message
        self._debugging_info = debugging_info
        self._errors = errors
        self._header = header

    @property
    def status_code(self) -> int:
        return self._status

    @property
    def detail(self) -> str:
        return self._message

    def to_json(self):
        return {
            "status_code": self._status,
            "reason": self._reason,
            "message": self._message,
        }

    @staticmethod
    def create_forbidden(
        message: str = "The user is not permitted to perform this action.",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.FORBIDDEN,
            reason="Forbidden.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_unauthorized(
        message: str = "The user is not authorized to perform this action.",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.UNAUTHORIZED,
            reason="Unauthorized",
            message=message,
            header=header,
        )

    @staticmethod
    def create_precondition_failed(
        message: str = "Unprocessable entity.",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.PRECONDITION_FAILED,
            reason="Precondition failed.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_not_found(
        message: str = "Not found.",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.NOT_FOUND,
            reason="Not found.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_bad_request(
        message: str = "Bad requests.",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.BAD_REQUEST,
            reason="Bad request.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_gateway_timeout(
        message: str,
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.GATEWAY_TIMEOUT,
            reason="Gateway Timeout.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_conflict(
        message: str,
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.CONFLICT,
            reason="Conflict.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_payload_to_large(
        message: str = "Payload too large",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
            reason="Request entity to large.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_unprocessable_enitity(
        message: str = "Unprocessable entity",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.UNPROCESSABLE_ENTITY,
            reason="Unprocessable entity.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_too_many_request(
        message: str = "Too Many Requests",
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.TOO_MANY_REQUESTS,
            reason="Too Many Requests.",
            message=message,
            header=header,
        )

    @staticmethod
    def create_bad_gateway(
        message: str,
        header: typing.Optional[typing.Dict[str, str]] = None,
    ) -> "WebAppException":
        return WebAppException(
            status=HTTPStatus.BAD_GATEWAY,
            reason="Bad Gateway.",
            message=message,
            header=header,
        )
