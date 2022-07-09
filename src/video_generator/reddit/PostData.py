from array import array
from dataclasses import dataclass
from typing import List

@dataclass()
class PostDataDto:
    id: str
    title: str
    content: List[str]

    def get_content_length(self) -> int:
        count = 0
        for p in self.content:
            count += len(p)

        return count