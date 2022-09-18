from typing import List
from environment import TEXT_CONFIG
from common.SentenceInfo import SentenceInfo

def get_text_overlay_filter(text: str, start_time: float, end_time: float, x: int, y: int) -> str:
    font_size = TEXT_CONFIG.FONT_SIZE
    font_color = TEXT_CONFIG.FONT_COLOR

    timing_config = f"enable='between(t,{start_time},{end_time})'"
    styling_config = f"fontsize={font_size}:fontcolor={font_color}"
    return f"drawtext=text='{text}':{styling_config}:x={x}:y={y}:{timing_config}"

def convert_seconds_to_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def get_input_command(path: str, end_time: str) -> str:
	return f'-t {end_time} -i "{path}"'

def get_audio_input(sentences: List[SentenceInfo]) -> str:
	inputs = []
	for s in sentences:
		inputs.append(f'-i "{s.audio_path}"')

	return " ".join(inputs)

def get_audio_concat(start_index: int, end_index: int, final_name: str) -> str:
	no_streams = end_index - start_index + 1
	filter = ""
	for i in range(start_index, end_index + 1):
		filter += f'[{i}:a]'
	filter += f'concat=n={no_streams}:v=0:a=1'
	filter += final_name

	return filter