
import logging
import pdb
from reddit.PostData import PostDataDto
from reddit.filtering_pipeline.filters import CharacterCount, MergeLines, UnusedPost


class FilterPipeline:
    FILTERS = [MergeLines, CharacterCount, UnusedPost]

    def __init__(self, posts: PostDataDto):
        self.posts = posts

    def start(self):
        for filter in FilterPipeline.FILTERS:
            initial_count = len(self.posts)
            
            f = filter(self.posts)
            self.posts = f.run()
            
            final_count = len(self.posts)
            logging.info(f'{filter.__name__} removed {initial_count - final_count} posts.')

    def get_results(self):
        self.start()
        return self.posts
