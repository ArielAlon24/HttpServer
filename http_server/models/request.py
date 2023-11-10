"""
Name: Ariel Alon
Description:
    This module defines the 'Request' class and all related methods.
"""

from ..enums.methods import Method

from typing import Dict, Optional


class Request:
    """
    A class that represents an HTTP request.

    Attributes:
        CARRIAGE_RETURN (str): A carriage return string.
        PAYLOAD_KEY (str): A key for injecting the payload into a function.
        HEADERS_KEY (str): A key for injecting the headers into a function.
        method (Method): Request's HTTP method.
        version (str): Request's HTTP version.
        path (str): Request's path.
        parameters (Optional[Dict[str, str]]):
            Request's optional parameters as a str-str mapping.
        headers (Optional[Dict[str, str]]):
            Request's optional headers as a str-str mapping.
        payload (Optional[str]): Request's payload.
    """

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
    ) -> None:
        """
        Initialize a Request.

        Parameters:
            method (Method): Request's HTTP method.
            version (str): Request's HTTP version.
            path (str): Request's path.
            parameters (Optional[Dict[str, str]]):
                Request's optional parameters as a str-str mapping.
            headers (Optional[Dict[str, str]]):
                Request's optional headers as a str-str mapping.
            payload (Optional[str]): Request's payload.

        """
        self.method = method
        self.version = version
        self.path = path
        self.parameters = parameters if parameters else {}
        self.headers = headers if headers else {}
        self.payload = payload

    def header(self) -> str:
        """
        Format the header of a request.

        Returns:
            str: The string format.
        """
        if self.parameters:
            full_path = f"{self.path}?" + "&".join(
                [f"{key}={value}" for key, value in self.parameters.items()]
            )
        else:
            full_path = self.path
        return f"{self.method.name} {full_path} {self.version}"

    def __str__(self) -> str:
        """
        Generate the string representation of a request.

        Returns:
            str: The string representation.
        """
        header = self.header() + self.CARRIAGE_RETURN
        headers = self.CARRIAGE_RETURN.join(
            [f"{key}: {value}" for key, value in (self.headers).items()]
        )
        payload = (
            f"{self.CARRIAGE_RETURN * 2}{self.payload}" if self.payload else ""
        )

        return f"{header}{headers}{payload}"
