from functools import reduce
import os
from typing import List
from uuid import uuid4
from generation.GenerationConfiguration import GenerationConfigurationDto
from environment import END_TIME_OFFSET, tmp_dir
from subprocess import check_call
import logging

from common.SentenceInfo import SentenceInfo
from .ffmpeg_helper import get_audio_input, get_input_command, \
							get_audio_concat, get_text_filter

def get_end_time(sentences: List[SentenceInfo]) -> float:
	return reduce(lambda acc, s: acc + s.length, sentences, 0)


def generate(configuration: GenerationConfigurationDto):
	logging.info('[Generation] Starting generation with configuration: ' + str(configuration))

	video_path = configuration.local_video_path
	sentences = configuration.sentences
	no_sentences = len(sentences)

	video_end_time = get_end_time(sentences) + END_TIME_OFFSET
	output_path = os.path.join(tmp_dir, uuid4().hex + '.mp4')

	final_audio_name = "[audio_final]"
	final_video_name = "[video_final]"
	ffmpeg_cmd = f"""
		ffmpeg \
		{get_input_command(video_path, video_end_time)} \
		{get_audio_input(sentences)} \
		-filter_complex "{get_audio_concat(1, no_sentences, final_audio_name)};[0:v]crop=ih*(9/16):ih{final_video_name};{get_text_filter(sentences, final_video_name, final_video_name)}" \
		-map {final_video_name} -map {final_audio_name} \
		-c:a aac -c:v libx264 -preset ultrafast -crf 23 \
		"{output_path}" -shortest -y
	"""
	

	logging.info('[Generation] Starting ffmpeg process with command: ' + ffmpeg_cmd)
	check_call(ffmpeg_cmd, shell=True)
	logging.info(f'[Generation] Ffmpeg process finished. Output file is: {output_path}')

	return output_path