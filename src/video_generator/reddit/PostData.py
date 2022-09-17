from dataclasses import dataclass
import hashlib
import pdb
from typing import List


@dataclass()
class PostDataDto:
    id: str
    title: str
    lines: List[str]
    content: str

    def get_content_length(self) -> int:
        count = 0
        for p in self.lines:
            count += len(p)

        return count
