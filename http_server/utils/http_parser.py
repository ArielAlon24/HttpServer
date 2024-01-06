from ..enums.methods import STRING_TO_METHOD, Method
from ..enums.header_types import HeaderType
from ..enums.cookie_attributes import CookieAttribute
from ..models.request import Request
from ..models.cookie import Cookie
from .date import DateUtils

from typing import Dict, List, Tuple
from datetime import datetime


class HttpParser:
    @classmethod
    def parse(cls, request: str) -> Request:
        lines = request.splitlines()
        if len(lines) == 0:
            raise ValueError("Encountered empty request")
        method, path, version = cls._parse_header(lines[0])
        path, parameters = cls._parse_parameters(path)
        headers, cookies, payload_start = cls._parse_headers(lines)
        payload = cls._parse_payload(lines, payload_start)
        return Request(
            method=method,
            path=path,
            version=version,
            parameters=parameters if parameters else None,
            headers=headers if headers else None,
            cookies=cookies if cookies else None,
            payload=payload,
        )

    @classmethod
    def _parse_header(cls, header: str) -> Tuple[Method, str, str]:
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

    @classmethod
    def _parse_parameters(cls, path: str) -> Tuple[str, Dict[str, str]]:
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

    @classmethod
    def _parse_headers(
        cls,
        lines: List[str],
    ) -> Tuple[Dict[str, str], Dict[str, Cookie], int]:
        headers = {}
        payload_start = 0
        str_cookies = []
        for index, line in enumerate(lines[1:]):
            if not line:
                payload_start = index + 1
                break
            key_value = line.split(": ")
            if len(key_value) != 2:
                raise ValueError(f"Incorrect use of headers: {key_value}")
            key, value = line.split(": ")
            if key == HeaderType.COOKIE.value:
                str_cookies.append(value)
            else:
                headers[key] = value

        cookies = cls._parse_cookies(str_cookies)
        return headers, cookies, payload_start

    @classmethod
    def _parse_cookies(cls, str_cookies: List[str]) -> Dict[str, Cookie]:
        cookies = {}
        for cookie_str in str_cookies:
            parts = cookie_str.split(";")
            first_pair = parts[0].split("=")
            if len(first_pair) != 2:
                raise ValueError(f"Could not parse Cookie: {cookie_str}")
            name, value = first_pair
            cookie_attrs = cls._parse_cookie_attributes(parts[1:])
            cookies[name] = Cookie(name=name, value=value, **cookie_attrs)

        return cookies

    @classmethod
    def _parse_cookie_attributes(cls, attr_list: List[str]) -> Dict:
        attributes: Dict[str, str | datetime | bool] = {}
        for attr in attr_list:
            if "=" in attr:
                key, value = attr.split("=")
                key = key.strip().lower()
                value = value.strip()

                if key in [
                    CookieAttribute.EXPIRES.value,
                    CookieAttribute.MAX_AGE.value,
                ]:
                    attributes[CookieAttribute.EXPIRES.value] = DateUtils.from_rfc7321(
                        value
                    )
                elif key == CookieAttribute.SAME_SITE.value:
                    attributes[CookieAttribute.SAME_SITE.value] = value
                elif key in [
                    CookieAttribute.DOMAIN.value,
                    CookieAttribute.PATH.value,
                ]:
                    attributes[key] = value
                else:
                    raise ValueError(
                        f"Unrecognized key and value attibutes: {key}={value}"
                    )
            else:
                attr = attr.strip().lower()
                if attr == CookieAttribute.SECURE.value:
                    attributes[CookieAttribute.SECURE.value] = True
                elif attr == CookieAttribute.HTTP_ONLY.value:
                    attributes[CookieAttribute.HTTP_ONLY.value] = True
                else:
                    raise ValueError(f"Unrecognized boolean attribute: {attr}.")
        return attributes

    @classmethod
    def _parse_payload(cls, lines: List[str], payload_start: int) -> str | None:
        payload = None
        if payload_start and payload_start < len(lines):
            payload = "\n".join(lines[payload_start:])
        return payload
