from subprocess import check_output


def get_audio_duration(path) -> float:
    ffmpeg_cmd = f'ffprobe -i "{path}" -show_streams -select_streams a:0'
    output = check_output(ffmpeg_cmd, shell=True).decode('utf-8')
    lines = output.split('\n')
    duration_line = list(filter(lambda line: line.startswith('duration='), lines))[0]
    duration = float(duration_line.split('=')[1])

    return duration