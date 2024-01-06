from ..enums import Method, HeaderType
from .cookie import Cookie

from typing import Dict, Optional


class Request:
    CARRIAGE_RETURN = "\r\n"
    PAYLOAD_KEY = "payload"
    HEADERS_KEY = "headers"
    COOKIES_KEY = "cookies"

    def __init__(
        self,
        method: Method,
        version: str,
        path: str,
        parameters: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, Cookie]] = None,
        payload: Optional[str] = None,
    ) -> None:
        self.method = method
        self.version = version
        self.path = path
        self.parameters = parameters if parameters else {}
        self.headers = headers if headers else {}
        self.cookies = cookies if cookies else {}
        self.payload = payload

    def header(self) -> str:
        if self.parameters:
            full_path = f"{self.path}?" + "&".join(
                [f"{key}={value}" for key, value in self.parameters.items()]
            )
        else:
            full_path = self.path
        return f"{self.method.name} {full_path} {self.version}"

    def __repr__(self) -> str:
        return (
            f"Request({self.header()}, "
            + f"Parameters: {self.parameters}, "
            + f"Headers: {self.headers}, "
            + f"Cookies: {self.cookies}, "
            + f"Payload: {self.payload})"
        )

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False

        return (
            self.method == other.method
            and self.version == other.version
            and self.path == other.path
            and self.parameters == other.parameters
            and self.headers == other.headers
            and self.cookies == other.cookies
            and self.payload == other.payload
        )
