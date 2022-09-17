import logging
import os
from typing import List
from reddit.filtering_pipeline.FilterProcessor import FilterProcessor
from reddit.PostData import PostDataDto

class CharacterCount(FilterProcessor):
    CHARACTERS_MIN_COUNT = os.environ.get('CHARACTERS_MIN_COUNT', 200)
    CHARACTERS_MAX_COUNT = os.environ.get('CHARACTERS_MAX_COUNT', 1500)
  
    def run(self) -> List[PostDataDto]:
        return list(
            filter(
                lambda p: p.get_content_length() >= CharacterCount.CHARACTERS_MIN_COUNT and
                            p.get_content_length() <= CharacterCount.CHARACTERS_MAX_COUNT, 
                self.posts))