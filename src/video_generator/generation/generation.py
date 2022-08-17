import os
from uuid import uuid4
from generation.GenerationConfiguration import GenerationConfigurationDto
from environment import ffmpeg_path, tmp_dir
from subprocess import check_call
import logging

def generate(configuration: GenerationConfigurationDto):
    logging.info('[Generation] Starting generation with configuration: ' + str(configuration))

    video_path = configuration.local_video_path
    voice_path = configuration.voice_path
    timestamps_path = configuration.timestamps_path

    output_path = os.path.join(tmp_dir, uuid4().hex + '.mp4')

    ffmpeg_cmd = f"""
        {ffmpeg_path} \
        -i "{video_path}" -t 00:00:10 \
        -i "{voice_path}" -t 00:00:10 \
        -vf "drawtext=text='Test text':x=20:y=20" \
        -map 0:v -map 1:a \
        -c:a aac -c:v libx264 -preset ultrafast -crf 23 \
        "{output_path}" -shortest -y
    """
    

    logging.info('[Generation] Starting ffmpeg process with command: ' + ' '.join(ffmpeg_cmd))
    check_call(ffmpeg_cmd, shell=True)
    logging.info(f'[Generation] Ffmpeg process finished. Output file is: {output_path}')