from enum import Enum


class Method(Enum):
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


STRING_TO_METHOD = {
    "CONNECT": Method.CONNECT,
    "DELETE": Method.DELETE,
    "GET": Method.GET,
    "HEAD": Method.HEAD,
    "OPTIONS": Method.OPTIONS,
    "POST": Method.POST,
    "PUT": Method.PUT,
    "TRACE": Method.TRACE,
}
