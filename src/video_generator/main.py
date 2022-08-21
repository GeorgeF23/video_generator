import os
from dotenv import load_dotenv

from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
from generation.GenerationConfiguration import GenerationConfigurationDto
load_dotenv()

from reddit.RedditClient import RedditClient
from text2speech.SpeechClient import SpeechClient
from generation.generation import generate
import logging
from environment import initialize_environment, tmp_dir
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

# print(SpeechClient.get_instance().get_text_to_speech("My boyfriend(M20)and me(F19) have been dating for 7 months,and I’ve noticed some weird interactions between him and his animals. As we started our relationship I’ve noticed he shows a lot of attention to his cats,like kisses and laying down with them as he would with me or calling them his girlfriends. We were talking on the phone one night and he was telling me about his female cats(he has two)we weren’t really talking that much until he said”you wanna know something I noticed about Jenny?”I replied yeah what is it?he said “Jenny doesn’t like when someone else touches her private parts,but when I do it she doesn’t mind”."))
# print(SpeechClient.get_instance().get_text_timestamps("My boyfriend(M20)and me(F19) have been dating for 7 months,and I’ve noticed some weird interactions between him and his animals. As we started our relationship I’ve noticed he shows a lot of attention to his cats,like kisses and laying down with them as he would with me or calling them his girlfriends. We were talking on the phone one night and he was telling me about his female cats(he has two)we weren’t really talking that much until he said”you wanna know something I noticed about Jenny?”I replied yeah what is it?he said “Jenny doesn’t like when someone else touches her private parts,but when I do it she doesn’t mind”."))

generate(GenerationConfigurationDto(
    os.path.join(tmp_dir, 'b9d1719cf09345c8a0cd1f6a7ab57064.webm'),
    os.path.join(tmp_dir, 'bce8b1a6158b4e0093cf77b82ad976b3.mp3'),
    os.path.join(tmp_dir, '02209ec6029540218a974e24680800f2.json')
))