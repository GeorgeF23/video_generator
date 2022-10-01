import logging
import os
from typing import List


tmp_dir = os.environ.get('TMP_DIR', 'tmp')

END_TIME_OFFSET = int(os.environ.get('END_TIME_OFFSET', '1'))
AUDIO_CUT_TIME = float(os.environ.get('AUDIO_CUT_TIME', '0.52'))

RESPONSE_QUEUE_URL = os.environ.get('GENERATION_RESPONSE_QUEUE', '')

class TEXT_CONFIG:
	FONT_PATH = os.environ.get('TEXT_FONT_PATH', 'resources/fonts/verdana.ttf')
	FONT_SIZE = int(os.environ.get('TEXT_FONT_SIZE', '35'))
	FONT_COLOR = os.environ.get('TEXT_FONT_COLOR', 'white')
	CHARS_PER_LINE = int(float(os.environ.get('TEXT_CHARS_PER_LINE_COEF', '0.8')) * int(os.environ.get('TEXT_FONT_SIZE', '')))
	CHARS_PER_SCREEN = int(float(os.environ.get('TEXT_CHARS_PER_SCREEN_COEF', '5.0')) * int(os.environ.get('TEXT_FONT_SIZE', '')))
	X_COEF = float(os.environ.get('TEXT_START_X', '0.1'))
	Y_COEF = float(os.environ.get('TEXT_START_Y', '0.1'))
	BOX=int(os.environ.get('BOX', '1'))
	BOX_W=int(os.environ.get('BOX_W', '20'))
	BOX_COLOR=os.environ.get('BOX_COLOR', 'black@0.3')

def check_env_dirs(dirs: List[str]) -> None:
	for dir in dirs:
		if not os.path.exists(dir):
			os.makedirs(dir)

def initialize_environment() -> None:
	check_env_dirs([tmp_dir])
	if len(logging.getLogger().handlers) > 0:
		logging.getLogger().setLevel(logging.DEBUG)
	else:
		logging.basicConfig(level=logging.DEBUG)
	logging.getLogger('botocore').setLevel(logging.WARNING)
	logging.getLogger('s3transfer').setLevel(logging.WARNING)
	