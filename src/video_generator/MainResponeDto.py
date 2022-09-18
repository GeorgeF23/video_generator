from dataclasses import dataclass


@dataclass
class MainResponseDto:
	status: str
	output_url: str
	error: str
