"""
Name: Ariel Alon
Description: This module has utility functions for parsing HTTP requests.
"""

from ..enums.methods import STRING_TO_METHOD, Method
from ..models.request import Request

from typing import Dict, List, Tuple


def parse(request: str) -> Request:
    """
    Parse an HTTP request.

    Parameters:
        request (str): HTTP request string.

    Returns:
        Request: The parsed request.
    """
    lines = request.splitlines()
    if len(lines) == 0:
        raise ValueError("Encountered empty request")
    method, path, version = _parse_header(lines[0])
    path, parameters = _parse_parameters(path)
    headers, payload_start = _parse_headers(lines)
    payload = _parse_payload(lines, payload_start)
    return Request(
        method=method,
        path=path,
        version=version,
        parameters=parameters if parameters else None,
        headers=headers if headers else None,
        payload=payload,
    )


def _parse_header(header: str) -> Tuple[Method, str, str]:
    """
    Parse an HTTP header.

    Parameters:
        header (str): HTTP request header string.

    Returns:
        Method: Header's method.
        str: Header's path.
        str: Header's version
    """
    header_parts = header.split(" ")
    if len(header_parts) != 3:
        raise ValueError(
            "Request must include a valid header. (<method> <path> <version>)"
        )

    method_str, path, version = header_parts

    if method_str not in STRING_TO_METHOD:
        raise ValueError(f"Unknown HTTP method {method_str}.")
    method = STRING_TO_METHOD[method_str]

    return method, path, version


def _parse_parameters(path: str) -> Tuple[str, Dict[str, str]]:
    """
    Parse an HTTP path.

    Parameters:
        path (str): HTTP request path string.

    Returns:
        str: Request's path.
        Dict[str, str]: Request's parameters mapping.
    """
    parameters: Dict[str, str] = {}
    if "?" in path:
        path_parts = path.split("?")
        path = path_parts[0]
        query_string = path_parts[1]

        for parameter in query_string.split("&"):
            key_value = parameter.split("=")
            if len(key_value) != 2:
                raise ValueError(f"Incorrect use of parameters: {key_value}")
            key, value = key_value
            parameters[key] = value

    return path, parameters


def _parse_headers(lines: List[str]) -> Tuple[Dict[str, str], int]:
    """
    Parse HTTP headers.

    Parameters:
        lines (List[str]): HTTP header lines.

    Returns:
        Dict[str, str]: Request's headers mapping.
        int: Payload start line.
    """
    headers: Dict[str, str] = {}
    payload_start = 0

    for index, line in enumerate(lines[1:]):
        if not line:
            payload_start = index + 1
            break
        key_value = line.split(": ")
        if len(key_value) != 2:
            raise ValueError(f"Incorrect use of headers: {key_value}")
        key, value = line.split(": ")
        headers[key] = value

    return headers, payload_start


def _parse_payload(lines: List[str], payload_start: int) -> str:
    """
    Parse an HTTP payload.

    Parameters:
        lines (str): HTTP request lines.
        payload_start (int): Payload's start line.

    Returns:
        str: Request's payload.
    """
    payload = None
    if payload_start and payload_start < len(lines):
        payload = "\n".join(lines[payload_start:])
    return payload
