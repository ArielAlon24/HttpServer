from typing import Callable, Tuple
from enums.content_types import ContentType
from dataclasses import dataclass


@dataclass
class Page:
    function: Callable[Tuple, str]
    content_type: ContentType
