def get_text_overlay_filter(text, x, y, start_time, end_time):
    timing_config = f"enable='between(t,{start_time},{end_time})'"
    styling_config = f"fontsize=50:fontcolor=white"
    return f"drawtext=text='{text}':{styling_config}:x={x}:y={y}:{timing_config}"