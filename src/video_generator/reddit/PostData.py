from array import array
from dataclasses import dataclass
from typing import List

@dataclass()
class PostDataDto:
    id: str
    title: str
    content: List[str]