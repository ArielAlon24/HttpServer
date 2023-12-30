from typing import Callable, Set, Dict
from .models.cookie import Cookie


class _WithCookies:
    def __init__(self, function: Callable) -> None:
        self.__name__ = function.__name__
        self.__annotations__ = function.__annotations__
        self.function = function
        self.cookies: Set[Cookie] = set()
        self._instance = None

    def __get__(self, instance, _):
        self._instance = instance
        return self

    def __call__(self, *args, **kwargs):
        self.cookies.clear()
        if self._instance:
            return self.function(self._instance, *args, **kwargs)
        return self.function(*args, **kwargs)


with_cookies = _WithCookies


class _WithHeaders:
    def __init__(self, function: Callable) -> None:
        self.__name__ = function.__name__
        self.__annotations__ = function.__annotations__
        self.function = function
        self.headers: Dict[str, str] = {}
        self._instance = None

    def __get__(self, instance, _):
        self._instance = instance
        return self

    def __call__(self, *args, **kwargs):
        self.headers.clear()
        if self._instance:
            return self.function(self._instance, *args, **kwargs)
        return self.function(*args, **kwargs)


with_headers = _WithHeaders
