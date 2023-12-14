"""
Description:
    This module defines the 'Response' class and related methods.
"""
from __future__ import annotations

from .redirect import Redirect
from ..enums.status_code import StatusCode
from ..enums.content_types import ContentType
from ..enums.header_types import HeaderType
from ..utils import html
from ..utils import file
from ..utils import date

from typing import Dict, Optional
import traceback


class Response:
    """
    A class that represents an HTTP response.

    Attributes:
        CARRIAGE_RETURN (str): A carriage return string.
        VERSION (str): Response's HTTP version.
        status_code (StatusCode): Response's status code.
        headers (Optional[Dict[str, str]]):
            Request's optional headers as a str-str mapping.
        content (Optional[bytes]): Response's content.
        content_type (ContentType): Response's content type.
        auto_generated_headers (bool):
            A boolean representing whether headers will be auto generated.
    """

    VERSION: str = "HTTP/1.1"
    CARRIAGE_RETURN: str = "\r\n"

    def __init__(
        self,
        status_code: StatusCode,
        headers: Optional[Dict[str, str]] = None,
        content: Optional[bytes] = None,
        content_type: ContentType | None = None,
        auto_generated_headers: bool = True,
    ) -> None:
        """
        Initialize a Response.

        Parameters:
            status_code (StatusCode): Response's status code.
            headers (Optional[Dict[str, str]]):
                Request's optional headers as a str-str mapping.
            content (Optional[bytes]): Response's content.
            content_type (ContentType): Response's content type.
            auto_generated_headers (bool):
                A boolean representing whether headers will be auto generated.
        """
        self.status_code = status_code
        self.headers = headers if headers else {}
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
        """
        Initialize an error Response, this response if for developing purposes
        and adds the traceback of the exception to the response's payload.

        Parameters:
            status_code (StatusCode): Response's status code.
            error: (Exception):

        Returns:
            Response: An error Response.
        """
        content = f"""
        <!DOCTYPE html>
        <html lang="en">
           <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>Error</title>
           </head>
           <body>
              <h1>
                <pre>{repr(status_code)}</pre>
              </h1>
              <h2>
                <pre>{html.string_to_html(repr(error))}</pre>
              </h2>
              <pre>{html.string_to_html(traceback.format_exc())}</pre>
           </body>
        </html>
        """
        response = Response(
            status_code=status_code,
            content=content.encode(),
            content_type=ContentType.HTML,
        )
        response._generate_headers()
        return response

    @classmethod
    def from_redirect(cls, redirect: Redirect) -> Response:
        """
        Create a redirect response.

        Attributes:
            redirect (Redirect): Redirect object.

        Returns:
            A redirect response.
        """
        response = Response(status_code=redirect.status_code)
        response._generate_headers()
        response.headers[HeaderType.LOCATION.value] = redirect.location
        return response

    def _generate_headers(self) -> None:
        """
        Generate headers for a response.
        """
        if self.content and HeaderType.CONTENT_LENGTH.value not in self.headers:
            self.headers[HeaderType.CONTENT_LENGTH.value] = str(len(self.content))

        if self.content_type and HeaderType.CONTENT_TYPE.value not in self.headers:
            self.headers[HeaderType.CONTENT_TYPE.value] = self.content_type.value

        if HeaderType.DATE.value not in self.headers:
            self.headers[HeaderType.DATE.value] = date.rfc7321()

    def to_bytes(self) -> bytes:
        """
        Encode the response in the correct format.

        Returns:
            bytes: The encoded and formatted response.
        """
        status_line = (
            f"{self.VERSION} {repr(self.status_code)}{self.CARRIAGE_RETURN}"
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
