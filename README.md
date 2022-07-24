# Video generator
The application's goal is to create short (maybe long in the future) videos with a game in the background and a reddit text (maybe more sources in the future) over it.

### Table of contents
- [Video generator](#video-generator)
    + [1.Setup](#1setup)
      - [1.1 Installation](#11-installation)
      - [1.2 Running locally](#12-running-locally)
    + [2. Services](#2-services)
      - [2.1 Reddit API](#21-reddit-api)
      - [2.2 Text 2 speech](#22-text-2-speech)

### 1.Setup
#### 1.1 Installation

Install aws cli from the aws website and configure it with 'aws configure' by introducing the IAM credentials.

```bash
sudo apt install git bash curl python3 python3-pip wget curl
pip install --upgrade pip
pip install --upgrade awscli
pip install -r src/video_generator/requirements.txt
sudo ln -s /usr/bin/python3 /usr/bin/python # to use python insead of python3

# Install youtube-dl
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Install ffmpeg
sudo curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o /tmp/ffmpeg.tar.xz
sudo tar xvf /tmp/ffmpeg.tar.xz -C /tmp
sudo find /tmp -name "ffmpeg" -exec  cp {} /usr/local/bin ";"
sudo rm /tmp/ffmpeg.tar.xz
```

#### 1.2 Running locally

This application will run on AWS so to run locally you need to start some of them. 
To do that, run the 'start-localstack.sh' script that will launch some dockers containing ElasticSearch, Kibana (and more).

### 2. Services

The application is split among many services, all doing some independent work that is merged to create the final video.
The services that are involved in the video generation will run on an AWS lambda function.

#### 2.1 Reddit API

The main text that will be overlayed on the video comes from Reddit through Reddit's API.

The python reddit module exposes a RedditClient class that will be used to fetch posts from the reddit API. In addition, the PostData class will be used to store a reddit post data.

The flow is:
* a login request will be sent to reddit(https://www.reddit.com/api/v1/access_token) among some credentials
* upon sucessful login, reddit will send back an access token that will be used to make further interogations
* to fetch the posts, a request is made to https://oauth.reddit.com/r/{subreddit}/hot among with a number of posts to fetch added
* the received posts are filtered through a pipeline

The filter pipeline contains the following filters:
* CharacterCount - removes posts that are too short or too long
* UnusedPost - removes posts that were used in the past (used posts are stored in ElasticSearch)

The enviornment variables used by this service are (* are mandatory):

* REDDIT_CLIENT_ID* - obtained upon registering a Reddit APP
* REDDIT_SECRET* - obtained upon registering a Reddit APP
* REDDIT_USERNAME* - username of reddit account
* REDDIT_PASSWORD* - password of reddit account
* ELASITC_HOST* - URL of the elasticsearch service
* REDDIT_POSTS_INDEX* - index where used reddit posts will be stored
* CHARACTERS_MIN_COUNT - minimum character count of post
* CHARACTERS_MAX_COUNT - maximum character count of post

#### 2.2 Text 2 speech

For text to speech, AWS Polly is used using the voice 'Matthew' (maybe will make this customizable in the future).
Most of the voices have 2 engines: 'neural' which is better, but more expensive and 'standard'.
There is a free tier available: 1 million chars/month for neural and 5 million chars/month for standard.

For now, the default will be Matthew with neural engine. Maybe will make that configurable from frontend.