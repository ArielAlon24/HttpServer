"""
Description:
    This module contains an enum and a string mapping for HTTP methods.
"""


from enum import Enum
from typing import Dict


class Method(Enum):
    """
    An HTTP method enum.
    """

    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


# str to Method mapping
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
