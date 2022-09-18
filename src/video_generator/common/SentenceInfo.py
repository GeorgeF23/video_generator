from dataclasses import dataclass


@dataclass
class SentenceInfo:
	length: float
	audio_path: str
	text: str
