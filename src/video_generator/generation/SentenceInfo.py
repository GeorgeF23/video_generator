from dataclasses import dataclass


@dataclass
class SentenceInfo:
    start_time: int
    start_index: int
    end_index: int
    text: str