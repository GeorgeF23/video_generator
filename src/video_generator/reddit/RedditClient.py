import requests
from . import *

class RedditClient:

    def login(self):
        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_SECRET)
        data = {'grant_type': 'password',
                'username': REDDIT_USERNAME,
                'password': REDDIT_PASSWORD}

        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=self.headers)
        res_json = res.json()

        return res_json.get('access_token')

    def __init__(self):
        self.headers = {'User-Agent': APP_NAME}
        access_token = self.login()
        print(access_token)
        pass