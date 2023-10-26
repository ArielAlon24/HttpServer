from typing import Callable, Tuple
from dataclasses import dataclass
from enums.content_types import ContentType


@dataclass
class Resource:
    function: Callable[Tuple, str]
    content_type: ContentType
