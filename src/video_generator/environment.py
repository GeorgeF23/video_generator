import os
from tempfile import gettempdir
from typing import List


tmp_dir = os.environ.get('TMP_DIR', gettempdir())
ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

END_TIME_OFFSET = int(os.environ.get('END_TIME_OFFSET'))

class TEXT_CONFIG:
    FONT_SIZE = int(os.environ.get('TEXT_FONT_SIZE'))
    FONT_COLOR = os.environ.get('TEXT_FONT_COLOR')
    CHARS_PER_LINE = float(os.environ.get('TEXT_CHARS_PER_LINE_COEF')) * int(os.environ.get('TEXT_FONT_SIZE'))
    LINES_PER_SCREEN = int(os.environ.get('TEXT_LINES_PER_SCREEN'))
    X = int(os.environ.get('TEXT_START_X'))
    Y = int(os.environ.get('TEXT_START_Y'))

def check_env_dirs(dirs: List[str]) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def initialize_environment() -> None:
    check_env_dirs([tmp_dir])
    # TODO: add dotenv here