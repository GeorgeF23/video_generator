from typing import List
from reddit.filtering_pipeline.FilterProcessor import FilterProcessor
from reddit.PostData import PostDataDto

class RemoveEdits(FilterProcessor):
	def run(self) -> List[PostDataDto]:
		for post in self.posts:
			post.lines = [line for line in post.lines if not line.startswith('Edit:')]
		return self.posts