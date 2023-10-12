from enum import Enum
from typing import Dict


class Method(Enum):
    CONNECT: str = "Connect"
    DELETE: str = "Delete"
    GET: str = "Get"
    HEAD: str = "Head"
    OPTIONS: str = "Options"
    POST: str = "Post"
    PUT: str = "Put"
    TRACE: str = "Trace"


STRING_TO_METHOD: Dict[str, Method] = {
    "CONNECT": Method.CONNECT,
    "DELETE": Method.DELETE,
    "GET": Method.GET,
    "HEAD": Method.HEAD,
    "OPTIONS": Method.OPTIONS,
    "POST": Method.POST,
    "PUT": Method.PUT,
    "TRACE": Method.TRACE,
}
