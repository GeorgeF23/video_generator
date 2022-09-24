import hashlib
from typing import List
import requests
import logging

from reddit.exceptions import RedditAuthenticaionError
from common.html_beautify.html_beautify import beautify
from reddit.PostData import PostDataDto
from reddit.filtering_pipeline.FilterPipeline import FilterPipeline
from . import *

class RedditClient:

    def __init__(self):
        self.headers = {'User-Agent': APP_NAME}
        access_token = self.login()
        self.headers = {**self.headers, **{'Authorization': f"bearer {access_token}"}}

    def login(self):
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)  # type: ignore
        data = {'grant_type': 'password',
                'username': REDDIT_USERNAME,
                'password': REDDIT_PASSWORD}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.headers)  # type: ignore
        res_json = res.json()
        token = res_json.get('access_token')
        logging.debug(f'Got login response from REDDIT: {res_json}')

        if not token:
            raise RedditAuthenticaionError(f'Error while authentication to Reddit: {res_json}')

        logging.info('Successfully logged into Reddit')
        return token

    def fetch_posts(self, subreddit: str, count: int) -> List[PostDataDto]:
        res = requests.get(f'https://oauth.reddit.com/r/{subreddit}/hot', headers=self.headers, params={'limit': f'{count}'})  # type: ignore
        res.raise_for_status()

        posts = []
        for post in res.json()['data']['children']:
            try:
                id = hashlib.md5(post['data']['permalink'].encode()).hexdigest()
                title = post['data']['title']
                lines = beautify(post['data']['selftext_html'])
                post_data = PostDataDto(id, title, lines, "")

                posts.append(post_data)
            except:
                logging.debug('Got an invalid post')

        return posts

    def get_posts(self, subreddit: str, count: int) -> List[PostDataDto]:
        posts = self.fetch_posts(subreddit, count)
        filter_pipeline = FilterPipeline(posts)

        return filter_pipeline.get_results()