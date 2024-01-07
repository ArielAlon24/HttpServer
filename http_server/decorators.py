from typing import Callable, Set, Dict
from .models.cookie import Cookie
import inspect


class _InjectedFunction:
    def __init__(
        self, function: Callable, cookies: bool = False, headers: bool = False
    ) -> None:
        self.__name__ = function.__name__
        self.__annotations__ = function.__annotations__
        self.__doc__ = function.__doc__
        self.function = function
        if cookies:
            self.cookies: Set[Cookie] = set()
        if headers:
            self.headers: Dict[str, str] = {}
        self._instance = None
        self.__signature__ = inspect.signature(function)

    def __get__(self, instance, _):
        self._instance = instance
        return self

    def __call__(self, *args, **kwargs):
        if self._instance:
            return self.function(self._instance, *args, **kwargs)
        return self.function(*args, **kwargs)


def inject(cookies: bool = False, headers: bool = False):
    def decorator(function: Callable) -> _InjectedFunction:
        injected_function = _InjectedFunction(
            function=function, cookies=cookies, headers=headers
        )
        return injected_function

    return decorator
