import dataclasses
from email import message
import enum
import json
import os
import textwrap
from typing import List
from dotenv import load_dotenv

load_dotenv()

from generation.GenerationConfiguration import GenerationConfigurationDto
from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
from common.sqs import SqsClient
from common.SentenceInfo import SentenceInfo
from common.resources import get_audio_duration
from MainRequestDto import MainRequestDto
from reddit.PostData import PostDataDto
from environment import initialize_environment, tmp_dir, TEXT_CONFIG, AUDIO_CUT_TIME, RESPONSE_QUEUE_URL
from MainResponeDto import MainResponseDto
initialize_environment()

from reddit.RedditClient import RedditClient
from text2speech.SpeechClient import SpeechClient
from generation.generation import generate
import logging
from common.resources.resources_manager import download_resource
from common.s3 import S3Client
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

class InvokeType(enum.Enum):
	UNKNOWN = 0
	API = 1
	SNS = 2

def get_post(subreddit: str) -> PostDataDto:
	try_count = 1
	r = RedditClient()
	posts = []
	while len(posts) == 0:
		posts = r.get_posts(subreddit, try_count)
		try_count += 1

	# es_client = ElasticSearchClient.get_instance()
	# es_client.upload(posts, lambda post: post.id, 'reddit_posts')
	return posts[0]

def get_sentences(text: str) -> List[SentenceInfo]:
	split_text = textwrap.fill(text, width=TEXT_CONFIG.CHARS_PER_SCREEN).split('\n')
	sentences = []
	for t in split_text:
		audio_path = SpeechClient.get_instance().get_text_to_speech('george' + t + 'george')
		audio_length = get_audio_duration(audio_path) - AUDIO_CUT_TIME * 2
		s = SentenceInfo(audio_length, audio_path, t)
		sentences.append(s)
	return sentences


def main(request: MainRequestDto):
	response = None
	try:
		post = get_post(request.subreddit)
		video_url = download_resource(request.video_url)
		if video_url is None:
			raise RuntimeError(f'Video not found')

		sentences = get_sentences(post.content)

		output_path = generate(GenerationConfigurationDto(
			video_url,
			sentences
		))

		logging.info(f'Got final video: {output_path}')

		s3_url = S3Client.get_instance().upload_file(output_path)
		response = MainResponseDto("success", s3_url, "")
		return response
	except Exception as err:
		logging.error(f'[handler] Got error: {err}')
		response = MainResponseDto("error", "", str(err))
	
	return response

def get_http_request(event):
	request_str = event['body']
	return MainRequestDto(**json.loads(request_str))

def get_sns_request(event):
	message = event['Records'][0]['Sns']['Message']
	return MainRequestDto(**json.loads(message))

def get_request(event):
	if 'body' in event:
		logging.info('Invoked by API')
		return get_http_request(event), InvokeType.API
	elif 'Records' in event:
		logging.info('Invoked by SNS')
		return get_sns_request(event), InvokeType.SNS
	else:
		return None, InvokeType.UNKNOWN

def send_response(response: dict, type: InvokeType):
	if type == InvokeType.API:
		return {
			"statusCode": 200,
			"headers": {
				"Content-Type": "application/json"
			},
			"body": json.dumps(response)
		}
	elif type == InvokeType.SNS:
		sqs_client = SqsClient.get_instance()
		sqs_client.send_message(json.dumps(response), RESPONSE_QUEUE_URL)

def handler(event, _):
	logging.info(event)
	response = None
	request, invoke_type = get_request(event)
	
	if request:
		logging.info(f'Got request: {request}')
		response = main(request)
	else:
		response = MainResponseDto("error", "", "Could not get request")
	response = dataclasses.asdict(response)
	logging.info(f'Response is: {response}')
	
	return send_response(response, invoke_type)

if __name__ == '__main__':
	r = main(MainRequestDto('s3://main-video-generator/background_videos/49c5edd626204e5e8f912f34e36546e6.webm', 'confessions'))
	print(dataclasses.asdict(r))	
	print(json.dumps(dataclasses.asdict(r)))

