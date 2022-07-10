import logging
import os
from reddit.filtering_pipeline.FilterProcessor import FilterProcessor

class CharacterCount(FilterProcessor):
    CHARACTERS_MIN_COUNT = os.environ.get('CHARACTERS_MIN_COUNT', 200)
    CHARACTERS_MAX_COUNT = os.environ.get('CHARACTERS_MAX_COUNT', 1500)
  
    def run(self):
        return list(
            filter(
                lambda p: p.get_content_length() >= CharacterCount.CHARACTERS_MIN_COUNT and
                            p.get_content_length() <= CharacterCount.CHARACTERS_MAX_COUNT, 
                self.posts))