from dataclasses import dataclass
import hashlib
import pdb
from typing import List

@dataclass()
class PostDataDto:
    id: str
    title: str
    content: str

    def get_content_length(self) -> int:
        count = 0
        for p in self.content:
            count += len(p)

        return count