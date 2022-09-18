import os
from tempfile import gettempdir
from typing import List


tmp_dir = os.environ.get('TMP_DIR', gettempdir())
ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

END_TIME_OFFSET = int(os.environ.get('END_TIME_OFFSET', '1'))

class TEXT_CONFIG:
	FONT_PATH = os.environ.get('TEXT_FONT_PATH', '')
	FONT_SIZE = int(os.environ.get('TEXT_FONT_SIZE', '40'))
	FONT_COLOR = os.environ.get('TEXT_FONT_COLOR', 'white')
	CHARS_PER_LINE = int(float(os.environ.get('TEXT_CHARS_PER_LINE_COEF', '1.3')) * int(os.environ.get('TEXT_FONT_SIZE', '40')))
	CHARS_PER_SCREEN = int(float(os.environ.get('TEXT_CHARS_PER_SCREEN_COEF', '1.3')) * int(os.environ.get('TEXT_FONT_SIZE', '40')))
	X_COEF = float(os.environ.get('TEXT_START_X', '0.1'))
	Y_COEF = float(os.environ.get('TEXT_START_Y', '0.3'))

def check_env_dirs(dirs: List[str]) -> None:
	for dir in dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)

def initialize_environment() -> None:
	check_env_dirs([tmp_dir])
	# TODO: add dotenv here