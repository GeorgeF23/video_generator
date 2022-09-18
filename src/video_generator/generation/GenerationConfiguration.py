from dataclasses import dataclass
from typing import List

from common.SentenceInfo import SentenceInfo

@dataclass()
class GenerationConfigurationDto:
	local_video_path: str
	sentences: List[SentenceInfo]
