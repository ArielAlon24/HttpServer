from ..enums.methods import STRING_TO_METHOD, Method
from ..enums.header_types import HeaderType
from ..enums.cookie_attributes import CookieAttribute
from ..models.request import Request
from ..models.cookie import Cookie
from .date import DateUtils

from typing import Dict, List, Tuple
from datetime import datetime


def parse(request: str) -> Request:
    lines = request.splitlines()
    if len(lines) == 0:
        raise ValueError("Encountered empty request")
    method, path, version = _parse_header(lines[0])
    path, parameters = _parse_parameters(path)
    headers, cookies, payload_start = _parse_headers(lines)
    payload = _parse_payload(lines, payload_start)
    return Request(
        method=method,
        path=path,
        version=version,
        parameters=parameters if parameters else None,
        headers=headers if headers else None,
        cookies=cookies if cookies else None,
        payload=payload,
    )


def _parse_header(header: str) -> Tuple[Method, str, str]:
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


def _parse_headers(
    lines: List[str],
) -> Tuple[Dict[str, str], Dict[str, Cookie], int]:
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

    cookies: Dict[str, Cookie] = {}
    if HeaderType.COOKIE.value in headers:
        cookies = _parse_cookies(headers[HeaderType.COOKIE.value])
        headers.pop(HeaderType.COOKIE.value)

    return headers, cookies, payload_start


def _parse_cookies(cookie_header: str) -> Dict[str, Cookie]:
    cookies = {}
    for cookie_str in cookie_header.split("; "):
        parts = cookie_str.split(";")
        first_pair = parts[0].split("=")
        if len(first_pair) != 2:
            raise ValueError(f"Could not parse Cookie: {cookie_str}")
        name, value = first_pair
        cookie_attrs = _parse_cookie_attributes(parts[1:])

        max_age = None
        if isinstance(_value := cookie_attrs.get(CookieAttribute.MAX_AGE.value), int):
            max_age = _value

        expires = None
        if isinstance(
            _value := cookie_attrs.get(CookieAttribute.EXPIRES.value), datetime
        ):
            expires = _value

        domain = None
        if isinstance(_value := cookie_attrs.get(CookieAttribute.DOMAIN.value), str):
            domain = _value

        path = "/"
        if isinstance(_value := cookie_attrs.get(CookieAttribute.PATH.value), str):
            path = _value

        same_site = None
        if (
            str(_value := cookie_attrs.get(CookieAttribute.SAME_SITE.value))
            in Cookie.SAME_SITE_OPTIONS
        ):
            same_size = _value

        cookies[name] = Cookie(
            name=name,
            value=value,
            max_age=max_age,
            expires=expires,
            domain=domain,
            path=path,
            secure=CookieAttribute.SECURE.value in cookie_attrs,
            http_only=CookieAttribute.HTTP_ONLY.value in cookie_attrs,
            same_site=same_site,
        )

    return cookies


def _parse_cookie_attributes(
    attr_list: List[str],
) -> Dict[str, str | int | datetime]:
    attrs: Dict[str, str | int | datetime] = {}
    for attr in attr_list:
        if "=" in attr:
            key, value = attr.split("=")
            key = key.strip()
            value = value.strip()

            if key == CookieAttribute.MAX_AGE.value:
                attrs[key] = int(value)
            elif key == CookieAttribute.EXPIRES.value:
                attrs[key] = DateUtils.from_rfc7321(value)
            else:
                attrs[key] = value
        else:
            attrs[attr.strip()] = True
    return attrs


def _parse_payload(lines: List[str], payload_start: int) -> str | None:
    payload = None
    if payload_start and payload_start < len(lines):
        payload = "\n".join(lines[payload_start:])
    return payload
