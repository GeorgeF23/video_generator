import os
import textwrap
from typing import List
from uuid import uuid4
from environment import TEXT_CONFIG, tmp_dir
from common.SentenceInfo import SentenceInfo

def get_text_overlay_filter(text: str, start_time: float, end_time: float) -> str:
	font_size = TEXT_CONFIG.FONT_SIZE
	font_file = TEXT_CONFIG.FONT_PATH
	font_color = TEXT_CONFIG.FONT_COLOR
	x = TEXT_CONFIG.X_COEF
	y = TEXT_CONFIG.Y_COEF

	text = textwrap.fill(text, width=TEXT_CONFIG.CHARS_PER_LINE)

	text_path = os.path.join(tmp_dir, uuid4().hex)
	with open(text_path, 'w') as f:
		f.write(text)

	timing_config = f"enable='between(t,{start_time},{end_time})'"
	styling_config = f"fontsize={font_size}:fontcolor={font_color}:fontfile={font_file}"
	return f"drawtext=textfile='{text_path}':{styling_config}:x={x}*w:y={y}*h:{timing_config}"

def get_text_filter(sentences: List[SentenceInfo], source: str, dest: str) -> str:
	filters = []
	start_time = 0
	for s in sentences:
		end_time = start_time + s.length
		filters.append(get_text_overlay_filter(s.text, start_time, end_time))
		start_time = end_time

	filters_str = f'{dest};{dest}'.join(filters)
	return f'{source}{filters_str}{dest}'

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
