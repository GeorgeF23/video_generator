from dataclasses import dataclass
from enum import Enum

class ResponseStatus(Enum):
	SUCCESS = "success"
	ERROR = "error"

@dataclass
class MainResponseDto:
	status: ResponseStatus
	output_url: str
	error: str
