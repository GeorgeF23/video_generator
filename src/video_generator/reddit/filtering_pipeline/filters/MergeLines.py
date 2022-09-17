from reddit.filtering_pipeline.FilterProcessor import FilterProcessor


class MergeLines(FilterProcessor):
	def run(self):
		for post in self.posts:
			post.content = '\n'.join(post.content)

		return self.posts
