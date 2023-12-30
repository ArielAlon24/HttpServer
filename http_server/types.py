from typing import Callable, TypeVar

from .decorators import with_headers, with_cookies
from .models.redirect import Redirect


Content = str | bytes | None | Redirect
Creator = Callable[..., Content] | with_headers | with_cookies
CreatorType = TypeVar("CreatorType", bound=Creator)
