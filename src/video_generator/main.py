import os
from dotenv import load_dotenv
load_dotenv()

from reddit.RedditClient import RedditClient
import logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


r = RedditClient()
posts = r.get_posts('confessions', 2)
print(posts)
