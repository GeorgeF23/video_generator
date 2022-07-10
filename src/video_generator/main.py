import os
from dotenv import load_dotenv

from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
load_dotenv()

from reddit.RedditClient import RedditClient
import logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


r = RedditClient()
posts = r.get_posts('confessions', 2)

es_client = ElasticSearchClient.get_instance()
es_client.upload(posts, lambda post: post.id, 'reddit_posts')

print(es_client.get_by_id('f3e2baa2a6e20ccb62698bfdd2161fd3', 'reddit_posts'))