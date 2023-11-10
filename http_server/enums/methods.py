"""
Name: Ariel Alon
Description:
    This module contains an enum and a string mapping for HTTP methods.
"""


from enum import Enum
from typing import Dict


class Method(Enum):
    """
    An HTTP method enum.
    """

    CONNECT: str = "CONNECT"
    DELETE: str = "DELETE"
    GET: str = "GET"
    HEAD: str = "HEAD"
    OPTIONS: str = "OPTIONS"
    POST: str = "POST"
    PUT: str = "PUT"
    TRACE: str = "TRACE"


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
