
import logging
import pdb
from typing import List
from reddit.PostData import PostDataDto
from reddit.filtering_pipeline.filters import CharacterCount, UnusedPost, RemoveEdits
from reddit.filtering_pipeline.FilterProcessor import FilterProcessor


class FilterPipeline:
	FILTERS: List[FilterProcessor] = [RemoveEdits, CharacterCount, UnusedPost]

	def __init__(self, posts: PostDataDto):
		self.posts = posts

	def start(self):
		for filter in FilterPipeline.FILTERS:
			initial_count = len(self.posts)

			f = filter(self.posts)
			self.posts = f.run()

			final_count = len(self.posts)
			logging.info(
				f'{filter.__name__} removed {initial_count - final_count} posts.')

	def merge_lines(self):
		for post in self.posts:
			post.content = '\n'.join(post.lines)

	def get_results(self):
		self.start()
		self.merge_lines()
		return self.posts
