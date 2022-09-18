from functools import reduce
import os
from typing import List
from uuid import uuid4
from generation.GenerationConfiguration import GenerationConfigurationDto
from environment import END_TIME_OFFSET, ffmpeg_path, tmp_dir, TEXT_CONFIG
from subprocess import check_call
import logging

from common.SentenceInfo import SentenceInfo
from .ffmpeg_helper import convert_seconds_to_time, get_audio_input, get_text_overlay_filter, get_input_command, \
							get_audio_concat

def get_end_time(sentences: List[SentenceInfo]) -> float:
	return reduce(lambda acc, s: acc + s.length, sentences, 0)

def generate(configuration: GenerationConfigurationDto):
	logging.info('[Generation] Starting generation with configuration: ' + str(configuration))

	video_path = configuration.local_video_path
	sentences = configuration.sentences
	no_sentences = len(sentences)

	video_end_time = convert_seconds_to_time(get_end_time(sentences) + END_TIME_OFFSET)
	output_path = os.path.join(tmp_dir, uuid4().hex + '.mp4')

	final_audio_name = "[audio_final]"
	ffmpeg_cmd = f"""
		{ffmpeg_path} \
		{get_input_command(video_path, video_end_time)} \
		{get_audio_input(sentences)} \
		-filter_complex "{get_audio_concat(1, no_sentences, final_audio_name)}" \
		-map 0:v -map {final_audio_name} \
		-c:a aac -c:v libx264 -preset ultrafast -crf 23 \
		"{output_path}" -shortest -y
	"""
	

	logging.info('[Generation] Starting ffmpeg process with command: ' + ffmpeg_cmd)
	check_call(ffmpeg_cmd, shell=True)
	logging.info(f'[Generation] Ffmpeg process finished. Output file is: {output_path}')