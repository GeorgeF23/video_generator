import os
from typing import List
from reddit.filtering_pipeline.FilterProcessor import FilterProcessor
from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
from reddit.PostData import PostDataDto

class UnusedPost(FilterProcessor):

    REDDIT_POSTS_INDEX = os.environ.get('REDDIT_POSTS_INDEX', 'reddit_posts')

    def run(self) -> List[PostDataDto]:
        es_client = ElasticSearchClient.get_instance()
        return list(filter(
            lambda p: (es_client.get_by_id(p.id, UnusedPost.REDDIT_POSTS_INDEX) is None),
            self.posts
        ))