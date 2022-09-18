import os
import textwrap
from typing import List
from dotenv import load_dotenv

from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
from generation.GenerationConfiguration import GenerationConfigurationDto
from common.SentenceInfo import SentenceInfo
from common.resources import get_audio_duration
from MainRequestDto import MainRequestDto
from reddit.PostData import PostDataDto
from environment import initialize_environment, tmp_dir, TEXT_CONFIG, AUDIO_CUT_TIME
load_dotenv()
initialize_environment()

from reddit.RedditClient import RedditClient
from text2speech.SpeechClient import SpeechClient
from generation.generation import generate
import logging
from common.resources.resources_manager import download_resource
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))



def get_post(subreddit: str) -> PostDataDto:
	try_count = 1
	r = RedditClient()
	posts = []
	while len(posts) == 0:
		posts = r.get_posts('confessions', try_count)
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


def handler(request: MainRequestDto):
	post = get_post(request.subreddit)
	video_url = download_resource(request.video_url, youtube=True)
	if video_url is None:
		raise RuntimeError(f'Video not found')

	sentences = get_sentences(post.content)

	output_path = generate(GenerationConfigurationDto(
		video_url,
		sentences
	))

	logging.info(f'Got final video: {output_path}')


if __name__ == '__main__':
	pass