"""
@Author:   YangCheng
@contact:  1248644045@qq.com
@Software: Y.C
@Time:     2020/7/21 15:29
"""

from pydantic import BaseModel, Field
from .status import Http


class ErrorResponse(BaseModel):
    code: int = Field(..., description="Error code")
    error: str = Field(..., description="Error name")
    message: str = Field(..., description="Error detail")


class FastapiError(Exception):

    def __init__(self, status: Http, msg: str):
        self._status = status
        self._msg = msg
        super(FastapiError, self).__init__(self.msg)

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def code(self) -> int:
        return self._status.value

    @property
    def name(self) -> str:
        return self._status.name

    @property
    def response(self):
        return {
            self.code: {
                'description': self.msg,
                'model': ErrorResponse,
            }
        }


class ClientError:
    class BadRequest400(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.BadRequest400, self).__init__(
                Http.STATUS_400_BAD_REQUEST, msg
            )

    class Unauthorized401(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.Unauthorized401, self).__init__(
                Http.STATUS_401_UNAUTHORIZED, msg
            )

    class PaymentRequired402(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.PaymentRequired402, self).__init__(
                Http.STATUS_402_PAYMENT_REQUIRED, msg
            )

    class Forbidden403(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.Forbidden403, self).__init__(
                Http.STATUS_403_FORBIDDEN, msg
            )

    class NotFound404(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.NotFound404, self).__init__(
                Http.STATUS_404_NOT_FOUND, msg
            )

    class MethodNotAllowed405(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.MethodNotAllowed405, self).__init__(
                Http.STATUS_405_METHOD_NOT_ALLOWED, msg
            )

    class NotAcceptable406(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.NotAcceptable406, self).__init__(
                Http.STATUS_406_NOT_ACCEPTABLE, msg
            )

    class ProxyAuthenticationRequired407(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.ProxyAuthenticationRequired407, self).__init__(
                Http.STATUS_407_PROXY_AUTHENTICATION_REQUIRED, msg
            )

    class RequestTimeout408(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.RequestTimeout408, self).__init__(
                Http.STATUS_408_REQUEST_TIMEOUT, msg
            )

    class Conflict409(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.Conflict409, self).__init__(
                Http.STATUS_409_CONFLICT, msg
            )

    class Gone410(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.Gone410, self).__init__(
                Http.STATUS_410_GONE, msg
            )

    class LengthRequired411(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.LengthRequired411, self).__init__(
                Http.STATUS_411_LENGTH_REQUIRED, msg
            )

    class PreconditionFailed412(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.PreconditionFailed412, self).__init__(
                Http.STATUS_412_PRECONDITION_FAILED, msg
            )

    class RequestEntityTooLarge413(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.RequestEntityTooLarge413, self).__init__(
                Http.STATUS_413_REQUEST_ENTITY_TOO_LARGE, msg
            )

    class RequestUriTooLong414(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.RequestUriTooLong414, self).__init__(
                Http.STATUS_414_REQUEST_URI_TOO_LONG, msg
            )

    class UnsupportedMediaType415(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.UnsupportedMediaType415, self).__init__(
                Http.STATUS_415_UNSUPPORTED_MEDIA_TYPE, msg
            )

    class RequestedRangeNotSatisfiable416(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.RequestedRangeNotSatisfiable416, self).__init__(
                Http.STATUS_416_REQUESTED_RANGE_NOT_SATISFIABLE, msg
            )

    class ExpectationFailed417(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.ExpectationFailed417, self).__init__(
                Http.STATUS_417_EXPECTATION_FAILED, msg
            )

    class UnprocessableEntity422(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.UnprocessableEntity422, self).__init__(
                Http.STATUS_422_UNPROCESSABLE_ENTITY, msg
            )

    class Locked423(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.Locked423, self).__init__(
                Http.STATUS_423_LOCKED, msg
            )

    class FailedDependency424(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.FailedDependency424, self).__init__(
                Http.STATUS_424_FAILED_DEPENDENCY, msg
            )

    class PreconditionRequired428(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.PreconditionRequired428, self).__init__(
                Http.STATUS_428_PRECONDITION_REQUIRED, msg
            )

    class TooManyRequests429(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.TooManyRequests429, self).__init__(
                Http.STATUS_429_TOO_MANY_REQUESTS, msg
            )

    class RequestHeaderFieldsTooLarge431(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.RequestHeaderFieldsTooLarge431, self).__init__(
                Http.STATUS_431_REQUEST_HEADER_FIELDS_TOO_LARGE, msg
            )

    class UnavailableForLegalReasons451(FastapiError):
        def __init__(self, msg: str):
            super(ClientError.UnavailableForLegalReasons451, self).__init__(
                Http.STATUS_451_UNAVAILABLE_FOR_LEGAL_REASONS, msg
            )


class ServerError:
    class InternalServerError500(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.InternalServerError500, self).__init__(
                Http.STATUS_500_INTERNAL_SERVER_ERROR, msg
            )

    class NotImplemented501(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.NotImplemented501, self).__init__(
                Http.STATUS_501_NOT_IMPLEMENTED, msg
            )

    class BadGateway502(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.BadGateway502, self).__init__(
                Http.STATUS_502_BAD_GATEWAY, msg
            )

    class ServiceUnavailable503(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.ServiceUnavailable503, self).__init__(
                Http.STATUS_503_SERVICE_UNAVAILABLE, msg
            )

    class GatewayTimeout504(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.GatewayTimeout504, self).__init__(
                Http.STATUS_504_GATEWAY_TIMEOUT, msg
            )

    class InsufficientStorage507(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.InsufficientStorage507, self).__init__(
                Http.STATUS_507_INSUFFICIENT_STORAGE, msg
            )

    class NetworkAuthenticationRequired511(FastapiError):
        def __init__(self, msg: str):
            super(ServerError.NetworkAuthenticationRequired511, self).__init__(
                Http.STATUS_511_NETWORK_AUTHENTICATION_REQUIRED, msg
            )


class RetryableError(Exception):
    def __index__(self, error: FastapiError):
        self._error = error

    @property
    def error(self) -> FastapiError:
        return self._error
