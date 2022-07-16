import os
from dotenv import load_dotenv

from common.elasticsearch.ElasticSearchClient import ElasticSearchClient
load_dotenv()

from reddit.RedditClient import RedditClient
from text2speech.SpeechClient import SpeechClient
import logging
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


# r = RedditClient()
# posts = r.get_posts('confessions', 7)
# print(posts)
# print(len(posts))

# es_client = ElasticSearchClient.get_instance()
# es_client.upload(posts, lambda post: post.id, 'reddit_posts')

print(SpeechClient.get_instance().get_text_to_speech("My boyfriend(M20)and me(F19) have been dating for 7 months,and I’ve noticed some weird interactions between him and his animals. As we started our relationship I’ve noticed he shows a lot of attention to his cats,like kisses and laying down with them as he would with me or calling them his girlfriends.We were talking on the phone one night and he was telling me about his female cats(he has two)we weren’t really talking that much until he said”you wanna know something I noticed about Jenny?”I replied yeah what is it?he said “Jenny doesn’t like when someone else touches her private parts,but when I do it she doesn’t mind”."))