from typing import Callable, TypeVar

from .decorators import _InjectedFunction
from .models.redirect import Redirect


Content = str | bytes | None | Redirect
Creator = Callable[..., Content] | _InjectedFunction
CreatorType = TypeVar("CreatorType", bound=Creator)
