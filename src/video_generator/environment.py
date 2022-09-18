import logging
import os
from tempfile import gettempdir
from typing import List


tmp_dir = os.environ.get('TMP_DIR', gettempdir())
ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

END_TIME_OFFSET = int(os.environ.get('END_TIME_OFFSET', ''))
AUDIO_CUT_TIME = float(os.environ.get('AUDIO_CUT_TIME', ''))

class TEXT_CONFIG:
	FONT_PATH = os.environ.get('TEXT_FONT_PATH', '')
	FONT_SIZE = int(os.environ.get('TEXT_FONT_SIZE', ''))
	FONT_COLOR = os.environ.get('TEXT_FONT_COLOR', '')
	CHARS_PER_LINE = int(float(os.environ.get('TEXT_CHARS_PER_LINE_COEF', '')) * int(os.environ.get('TEXT_FONT_SIZE', '')))
	CHARS_PER_SCREEN = int(float(os.environ.get('TEXT_CHARS_PER_SCREEN_COEF', '')) * int(os.environ.get('TEXT_FONT_SIZE', '')))
	X_COEF = float(os.environ.get('TEXT_START_X', ''))
	Y_COEF = float(os.environ.get('TEXT_START_Y', ''))
	BOX=int(os.environ.get('BOX', ''))
	BOX_W=int(os.environ.get('BOX_W', ''))
	BOX_COLOR=os.environ.get('BOX_COLOR', '')

def check_env_dirs(dirs: List[str]) -> None:
	for dir in dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)

def initialize_environment() -> None:
	check_env_dirs([tmp_dir])
	if len(logging.getLogger().handlers) > 0:
		logging.getLogger().setLevel(logging.INFO)
	else:
		logging.basicConfig(level=logging.INFO)