import os
import textwrap
from dotenv import load_dotenv

from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
from generation.GenerationConfiguration import GenerationConfigurationDto
from video_generator.common.SentenceInfo import SentenceInfo
from video_generator.common.resources import get_audio_duration
load_dotenv()

from reddit.RedditClient import RedditClient
from text2speech.SpeechClient import SpeechClient
from generation.generation import generate
import logging
from environment import initialize_environment, tmp_dir, TEXT_CONFIG
from common.resources.resources_manager import download_resource
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


# r = RedditClient()
# posts = r.get_posts('confessions', 7)
# print(posts)
# print(len(posts))

# es_client = ElasticSearchClient.get_instance()
# es_client.upload(posts, lambda post: post.id, 'reddit_posts')

# initialize_environment()
# download_resource('https://www.youtube.com/watch?v=qu8X8UxBjjM', youtube=True)
test = "Instead of being a dumb little pushover, who seems to get stepped on and bullied by others. Sometimes I wish I could be the one doing the pushing over. I know how awful this sounds, and this isn't me at all, but I get tired of being the one to get shoved around. The world is a tough place, and the mean ones always seem to get ahead."

split_text = textwrap.fill(test, width=TEXT_CONFIG.CHARS_PER_SCREEN).split('\n')
sentences = []
for t in split_text:
	audio_path = SpeechClient.get_instance().get_text_to_speech(t)
	audio_length = get_audio_duration(audio_path)
	s = SentenceInfo(audio_length, audio_path, t)
	print()

# mp3, timestamps = SpeechClient.get_instance().process_text(test)
# print(mp3)
# print(timestamps)

# generate(GenerationConfigurationDto(
#     os.path.join(tmp_dir, 'b9d1719cf09345c8a0cd1f6a7ab57064.webm'),
#     os.path.join(tmp_dir, 'bce8b1a6158b4e0093cf77b82ad976b3.mp3'),
#     os.path.join(tmp_dir, '02209ec6029540218a974e24680800f2.json')
# ))