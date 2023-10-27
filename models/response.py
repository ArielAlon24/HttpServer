from typing import Dict, Optional, Self
from models.status_codes import StatusCode
from enums.content_types import ContentType
from enums.header_types import HeaderType
from utils import html
from utils import file

import traceback


class Response:
    VERSION: str = "HTTP/1.1"
    CARRIAGE_RETURN: str = "\r\n"

    def __init__(
        self,
        status_code: StatusCode,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[bytes] = None,
        content_type: ContentType = ContentType.HTML,
        auto_generated_headers: bool = True,
    ) -> None:
        self.status_code = status_code
        self.headers = headers if headers else {}
        self.content = content
        self.content_type = content_type

        if auto_generated_headers:
            self._generate_headers()

    @classmethod
    def create_error(cls, status_code: StatusCode, error: Exception) -> Self:
        content = file.template(
            "resources/error.html",
            status=repr(status_code),
            error=html.string_to_html(repr(error)),
            traceback=html.string_to_html(traceback.format_exc()),
        )
        response = Response(
            status_code=status_code, content=content, content_type=ContentType.HTML
        )
        response._generate_headers()
        return response

    def _generate_headers(self) -> None:
        if self.content and HeaderType.CONTENT_LENGTH.value not in self.headers:
            self.headers[HeaderType.CONTENT_LENGTH.value] = len(self.content)

        if HeaderType.CONTENT_TYPE.value not in self.headers:
            self.headers[HeaderType.CONTENT_TYPE.value] = self.content_type.value

    def to_bytes(self) -> bytes:
        status_line = (
            f"{self.VERSION} {self.status_code.code} {self.status_code.message}{self.CARRIAGE_RETURN}"
        ).encode()
        headers = (
            self.CARRIAGE_RETURN.join(
                [f"{key}: {value}" for key, value in self.headers.items()]
            )
            + self.CARRIAGE_RETURN * 2
        ).encode()

        if self.content:
            return status_line + headers + self.content + self.CARRIAGE_RETURN.encode()
        return status_line + headers
