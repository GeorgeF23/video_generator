import requests
import logging

from reddit.exceptions import RedditAuthenticaionError
from . import *

class RedditClient:

    def __init__(self):
        self.headers = {'User-Agent': APP_NAME}
        access_token = self.login()
        self.headers = {**self.headers, **{'Authorization': f"bearer {access_token}"}}

    def login(self):
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
        data = {'grant_type': 'password',
                'username': REDDIT_USERNAME,
                'password': REDDIT_PASSWORD}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.headers)
        res_json = res.json()
        token = res_json.get('access_token')
        logging.debug(f'Got login response from REDDIT: {res_json}')

        if not token:
            raise RedditAuthenticaionError(f'Error while authentication to Reddit: {res_json}')

        logging.info('Successfully logged into Reddit')
        return token
