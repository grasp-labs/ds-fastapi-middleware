class DsMiddlewareBaseException(Exception):
    """Base exception class"""

    def __init__(self, message, code):
        self.message = message
        self.code = code


class AuditException(DsMiddlewareBaseException):
    """Raised when an audit exception occurs"""

    def __init__(self, message="Audit exception.", code=500):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)


class ValueErrorException(DsMiddlewareBaseException, ValueError):
    """Raised when a value error occurs"""

    def __init__(self, message="Value error.", code=400):
        self.message = message
        self.code = code
        super().__init__(self.message, self.code)
