from typing import Dict, Optional, Self
from enums.methods import Method


class Request:
    CARRIAGE_RETURN: str = "\r\n"

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
        self.parameters = parameters
        self.headers = headers
        self.payload = payload

    def __str__(self) -> str:
        if self.parameters:
            full_path = f"{self.path}?" + "&".join(
                [f"{key}={value}" for key, value in self.parameters.items()]
            )
        else:
            full_path = self.path

        request_line = f"{self.method} {full_path} {self.version}{self.CARRIAGE_RETURN}"
        header_lines = self.CARRIAGE_RETURN.join(
            [f"{key}: {value}" for key, value in (self.headers or {}).items()]
        )
        payload = f"{self.CARRIAGE_RETURN * 2}{self.payload}" if self.payload else ""

        return f"{request_line}{header_lines}{payload}"
