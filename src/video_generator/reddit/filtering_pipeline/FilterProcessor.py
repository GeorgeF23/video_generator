from abc import ABC, abstractmethod
import logging
from typing import List
from reddit.PostData import PostDataDto

class FilterProcessor(ABC):

    def __init__(self, posts: List[PostDataDto]):
        self.posts = posts
    
    @abstractmethod
    def run(self) -> List[PostDataDto]:
        return NotImplemented
