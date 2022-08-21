import os
from tempfile import gettempdir
from typing import List


tmp_dir = os.environ.get('TMP_DIR', gettempdir())
ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

text_config = {
    'fontsize': int(os.environ.get('TEXT_FONT_SIZE')),
    'fontcolor': os.environ.get('TEXT_FONT_COLOR'),
    'chars_per_line': float(os.environ.get('TEXT_CHARS_PER_LINE_COEF')) * int(os.environ.get('TEXT_FONT_SIZE')),
    'lines_per_screen': int(os.environ.get('TEXT_LINES_PER_SCREEN'))
}

def check_env_dirs(dirs: List[str]) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def initialize_environment() -> None:
    check_env_dirs([tmp_dir])
    # TODO: add dotenv here