from dataclasses import dataclass
from datetime import date


@dataclass
class Post:
    id: int = None
    author_id: int = None
    created: date = None
    title: str = None
    body: str = None
