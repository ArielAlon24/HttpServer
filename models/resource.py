from typing import Callable, Tuple
from enums.content_types import ContentType


class Resource:
    def __init__(
        self, function: Callable[Tuple, str], content_type: ContentType
    ) -> None:
        self.function = function
        self.content_type = content_type
