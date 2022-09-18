from dataclasses import dataclass

@dataclass
class MainRequestDto:
	video_url: str
	subreddit: str