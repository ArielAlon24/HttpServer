import pytest
from http_server.models import Request, Cookie
from http_server.enums import Method
from http_server.utils.http_parser import HttpParser


def test_get_index():
    string = "GET / HTTP/1.1\r\nHost: www.example.com\r\n"
    expected = Request(
        method=Method.GET,
        version="HTTP/1.1",
        path="/",
        headers={
            "Host": "www.example.com",
        },
    )

    actual = HttpParser.parse(string)

    assert actual == expected


def test_request_with_parameters():
    string = "GET /search?index=10 HTTP/1.1\r\nHost: www.example.com\r\n"
    expected = Request(
        method=Method.GET,
        version="HTTP/1.1",
        path="/search",
        parameters={"index": "10"},
        headers={"Host": "www.example.com"},
    )
    actual = HttpParser.parse(string)
    assert actual == expected


def test_request_with_cookies():
    string = "GET / HTTP/1.1\r\nHost: www.example.com\r\nCookie: sessionId=abc123\r\n"
    expected = Request(
        method=Method.GET,
        version="HTTP/1.1",
        path="/",
        headers={"Host": "www.example.com"},
        cookies={"sessionId": Cookie(name="sessionId", value="abc123")},
    )
    actual = HttpParser.parse(string)
    assert actual == expected


def test_invalid_request():
    string = "INVALID / HTTP/1.1\r\nHost: www.example.com\r\n"
    with pytest.raises(ValueError):
        HttpParser.parse(string)


def test_invalid_cookie():
    string = "GET / HTTP/1.1\r\nHost: www.example.com\r\nCookie: =\r\n"
    with pytest.raises(ValueError):
        HttpParser.parse(string)
