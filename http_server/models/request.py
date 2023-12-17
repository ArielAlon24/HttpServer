from ..enums.methods import Method
from ..enums.header_types import HeaderType
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

    def __str__(self) -> str:
        header = self.header() + self.CARRIAGE_RETURN
        headers = self.CARRIAGE_RETURN.join(
            [f"{key}: {value}" for key, value in (self.headers).items()]
        )
        cookies = self.CARRIAGE_RETURN.join(
            f"{HeaderType.COOKIE.value}: {cookie}" for cookie in self.cookies.values()
        )

        payload = ""
        if self.payload:
            payload = f"{self.CARRIAGE_RETURN * 2}{self.payload}"

        return f"{header}{headers}{cookies}{payload}"
