from __future__ import annotations

from .redirect import Redirect
from .cookie import Cookie
from ..enums import StatusCode, ContentType, HeaderType
from ..utils.html import HtmlUtils
from ..utils.date import DateUtils

from typing import Dict, Set
import traceback

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport"
            content="width=device-width,
            initial-scale=1.0"
      >
      <title>Error</title>
   </head>
   <body>
      <h1>
        <pre>{status_code}</pre>
      </h1>
      <h2>
        <pre>{error_html}</pre>
      </h2>
      <pre>{traceback_html}</pre>
   </body>
</html>
"""


class Response:
    VERSION = "HTTP/1.1"
    CARRIAGE_RETURN = "\r\n"
    HEADERS_KEY = "headers"
    COOKIES_KEY = "cookies"

    def __init__(
        self,
        status_code: StatusCode,
        headers: Dict[str, str] | None = None,
        cookies: Set[Cookie] | None = None,
        content: bytes | None = None,
        content_type: ContentType | None = None,
        auto_generated_headers: bool = True,
    ) -> None:
        self.status_code = status_code
        self.headers = headers if headers else {}
        self.cookies = cookies if cookies else set()
        self.content = content
        self.content_type = content_type

        if auto_generated_headers:
            self._generate_headers()

    @classmethod
    def from_error(
        cls,
        error: Exception,
        status_code: StatusCode = StatusCode.INTERNAL_SERVER_ERROR,
    ) -> Response:
        content = ERROR_TEMPLATE.format(
            status_code=repr(status_code),
            error_html=HtmlUtils.string_to_html(repr(error)),
            traceback_html=HtmlUtils.string_to_html(traceback.format_exc()),
        )
        response = Response(
            status_code=status_code,
            content=content.encode(),
            content_type=ContentType.HTML,
        )
        response._generate_headers()
        return response

    @classmethod
    def from_redirect(cls, redirect: Redirect) -> Response:
        response = Response(status_code=redirect.status_code)
        response._generate_headers()
        response.headers[HeaderType.LOCATION.value] = redirect.location
        return response

    def _generate_headers(self) -> None:
        if self.content and HeaderType.CONTENT_LENGTH.value not in self.headers:
            self.headers[HeaderType.CONTENT_LENGTH.value] = str(len(self.content))

        if self.content_type and HeaderType.CONTENT_TYPE.value not in self.headers:
            self.headers[HeaderType.CONTENT_TYPE.value] = self.content_type.value

        if HeaderType.DATE.value not in self.headers:
            self.headers[HeaderType.DATE.value] = DateUtils.rfc7321()

    def to_bytes(self) -> bytes:
        status_line = f"{self.VERSION} {repr(self.status_code)}{self.CARRIAGE_RETURN}"
        status_line_encoded = status_line.encode()

        header_lines = [f"{key}: {value}" for key, value in self.headers.items()]

        for cookie in self.cookies:
            header_lines.append(f"{HeaderType.SET_COOKIE.value}: {str(cookie)}")

        headers = self.CARRIAGE_RETURN.join(header_lines) + self.CARRIAGE_RETURN * 2
        headers_encoded = headers.encode()

        first_part = status_line_encoded + headers_encoded
        if not self.content:
            return first_part
        return first_part + self.content + self.CARRIAGE_RETURN.encode()
