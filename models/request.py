from typing import Dict, Optional, Self
from enums.methods import Method


class Request:
    CARRIAGE_RETURN: str = "\r\n"
    PAYLOAD_KEY: str = "payload"
    HEADERS_KEY: str = "headers"

    def __init__(
        self,
        method: Method,
        version: str,
        path: str,
        parameters: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[str] = None,
    ) -> Self:
        self.method = method
        self.version = version
        self.path = path
        self.parameters = parameters if parameters else {}
        self.headers = headers if headers else {}
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
        payload = f"{self.CARRIAGE_RETURN * 2}{self.payload}" if self.payload else ""

        return f"{header}{headers}{payload}"
