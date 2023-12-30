from ..enums import ContentType, StatusCode
from .redirect import Redirect

from typing import Callable


class Resource:
    def __init__(
        self,
        function: Callable[..., str | bytes | None | Redirect],
        content_type: ContentType,
        success_status: StatusCode,
    ) -> None:
        self.function = function
        self.content_type = content_type
        self.success_status = success_status
