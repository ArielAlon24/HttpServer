from typing import Dict, Optional
from enums.status_codes import StatusCode


class Response:
    VERSION: str = "HTTP/1.1"

    def __init__(
        self,
        status_code: StatusCode,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.status_message = status_code
        self.headers = headers
        self.content = content

    def __str__(self) -> str:
        status_line = (
            f"{self.VERSION} {self.status_code.code} {self.status_code.message}\r\n"
        )
        header_lines = "\r\n".join(
            [f"{key}: {value}" for key, value in (self.headers or {}).items()]
        )
        return (
            f"{status_line}{header_lines}\r\n" + f"{self.content}\r\n"
            if self.content
            else "\r\n"
        )
