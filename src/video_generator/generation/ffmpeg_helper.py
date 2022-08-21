from subprocess import check_output
from environment import TEXT_CONFIG
from .SentenceInfo import SentenceInfo

def get_text_overlay_filter(text: str, start_time: float, end_time: float, x: int, y: int) -> str:
    font_size = TEXT_CONFIG.FONT_SIZE
    font_color = TEXT_CONFIG.FONT_COLOR

    timing_config = f"enable='between(t,{start_time},{end_time})'"
    styling_config = f"fontsize={font_size}:fontcolor={font_color}"
    return f"drawtext=text='{text}':{styling_config}:x={x}:y={y}:{timing_config}"

def get_audio_duration(path) -> float:
    ffmpeg_cmd = f'ffprobe -i "{path}" -show_streams -select_streams a:0'
    output = check_output(ffmpeg_cmd, shell=True).decode('utf-8')
    lines = output.split('\n')
    duration_line = list(filter(lambda line: line.startswith('duration='), lines))[0]
    duration = float(duration_line.split('=')[1])

    return duration

def convert_seconds_to_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'