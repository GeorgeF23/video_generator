from environment import TEXT_CONFIG
from .SentenceInfo import SentenceInfo

def get_text_overlay_filter(sentence_info: SentenceInfo, x: int, y: int) -> str:
    font_size = TEXT_CONFIG.FONT_SIZE
    font_color = TEXT_CONFIG.FONT_COLOR

    start_time = sentence_info.start_time
    end_time = start_time + 7
    text = sentence_info.text

    timing_config = f"enable='between(t,{start_time},{end_time})'"
    styling_config = f"fontsize={font_size}:fontcolor={font_color}"
    return f"drawtext=text='{text}':{styling_config}:x={x}:y={y}:{timing_config}"