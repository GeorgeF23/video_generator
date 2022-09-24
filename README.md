# Video generator
The application's goal is to create short (maybe long in the future) videos with a game in the background and a reddit text (maybe more sources in the future) over it.

### Table of contents
- [Video generator](#video-generator)
    + [1.Setup](#1setup)
      - [1.1 Installation](#11-installation)
      - [1.2 Running locally](#12-running-locally)
    + [2. Modules](#2-modules)
      - [2.1 Reddit API](#21-reddit-api)
      - [2.2 Text 2 speech](#22-text-2-speech)
	  - [2.3 Video generation](#23-video-generation)
	+ [3. How it works](#3-how-it-works)
	+ [4. Environment](#4-environment)
	+ [5. Deployment](#5-deployment)

### 1.Setup
#### 1.1 Installation

Install aws cli from the aws website and configure it with 'aws configure' by introducing the IAM credentials.
Also, you need to install terraform for the deployment.

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
sudo find /tmp -name "ffprobe" -exec  cp {} /usr/local/bin ";"
sudo rm /tmp/ffmpeg.tar.xz
```

#### 1.2 Running locally

This application will run on AWS so to run locally you need to start some of them. 
To do that, run the 'start-localstack.sh' script that will launch some dockers containing ElasticSearch, Kibana (and more).

### 2. Modules

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
* RemoveEdits - removes the lines that start with 'Edit:'

#### 2.2 Text 2 speech

For text to speech, AWS Polly is used using the voice 'Matthew' (maybe will make this customizable in the future).
Most of the voices have 2 engines: 'neural' which is better, but more expensive and 'standard'.
There is a free tier available: 1 million chars/month for neural and 5 million chars/month for standard.

For now, the default will be Matthew with neural engine. Maybe will make that configurable from frontend.

#### 2.3 Video generation

This module handles the actual video generation. It's entrypoint is in the 'generation.py' files and it receives a GenerationConfigurationDto as a request.
The GenerationConfigurationDto should contain the followin fields:
* local_video_path - path to the background video
* sentences - list of SentenceInfo
	* length - length of the sentence in seconds
	* audio_path - path to the audio file
	* text - the actual sentence

With that input, the generator will make a ffmpeg command that will concatenate the audio files and overlay the text on the background video.
The response is the local path to the ouput video.

### 3. How it works
1. Using the reddit modules, a post is fetched from reddit.
2. The background video is downloaded
3. The text is split in shorter sentences that fit on the screen
4. Each sentence is passed to Amazon Polly for text 2 speech conversion
5. Some dummy words are placed at the start and end so the pronunciation is better
6. The generation configuration is passed to the generator
7. The output video is uploaded to S3

### 4. Environment
Some environment variables need to be set:
| Env variable | Description | Example value |
| ------------ | ----------- | ------------- |
| APP_NAME | A name for the application (for reddit api) | Video generator/0.0.1 |
| REDDIT_CLIENT_ID | From Reddit API | - |
| REDDIT_SECRET | From Reddit API | - |
| REDDIT_USERNAME | Username of Reddit account | - |
| REDDIT_PASSWORD | Password of Reddit account | - |
| ELASTIC_HOST | Hostname of elasticsearch (currently disabled) | http://localhost:9200 |
| REDDIT_POSTS_INDEX | Index where to store used posts | reddits_posts |
| TMP_DIR | Tmp directory where to store intermediary files | tmp |
| DOWNLOAD_TIMEOUT | A download timeout for background video in seconds | 60 |
| TEXT_FONT_SIZE | Font size of text | 35 |
| TEXT_FONT_COLOR | The color of the text | white |
| TEXT_CHAR_PER_LINE_COEF | A coefficient that determines the number of characters to draw on a line. This is multiplied with TEXT_FONT_SIZE to get the number of characters. | 0.8 |
| TEXT_CHARS_PER_SCREEN_COEF | A coefficient that determines the number of characters to draw on the screen at a given time. This is multiplied with TEXT_FONT_SIZE to get the number of characters. | 5.0 |
| TEXT_START_X | The x coordinate for the start of the text. This is multiplied with video width | 0.1 |
| TEXT_START_Y | The y coordinate for the start of the text. This is multiplied with video height | 0.1 |
| TEXT_FONT_PATH | The path to the font file to use for text rendering | resources/fonts/verdana.ttf |
| BOX | Whether or not to draw a box around the text | 1 |
| BOX_W | Padding of the box | 20 |
| BOX_COLOR | The color of the box | black@0.3 |
| END_TIME_OFFSET | An offset at the final of the video where text is not drawn (in seconds). | 1 |
| AUDIO_CUT_TIME | How much to cut for the dummy word to not be heard | 0.52 |
| S3_BUCKET | The default bucket where the resources will be stored | video-generator-bucket |

### 5. Deployment
The application is deployed in AWS using Terraform. The deployment configuration is in the 'deployment' folder.

When the code is changed, a new docker image must be built and uploaded to AWS ECR. To do that, run the following command:
```bash
./deployment/lambda/docker-update.sh
```

To deploy to AWS use the following command:
```bash
./deployment/terraform/apply.sh
```