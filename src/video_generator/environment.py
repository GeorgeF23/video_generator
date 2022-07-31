import os
from typing import List


tmp_dir = os.environ.get('TMP_DIR')
ffmpeg_path = os.environ.get('FFMPEG_PATH', 'ffmpeg')

def check_env_dirs(dirs: List[str]) -> None:
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def initialize_environment() -> None:
    check_env_dirs([tmp_dir])
    # TODO: add dotenv here