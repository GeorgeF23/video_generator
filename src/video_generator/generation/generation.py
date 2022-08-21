from functools import reduce
import json
import operator
import os
from typing import List
from uuid import uuid4
from generation.GenerationConfiguration import GenerationConfigurationDto
from environment import END_TIME_OFFSET, ffmpeg_path, tmp_dir, TEXT_CONFIG
from subprocess import check_call
import logging
import textwrap

from .SentenceInfo import SentenceInfo

from .ffmpeg_helper import convert_seconds_to_time, get_audio_duration, get_text_overlay_filter

def get_sentences_info(timestamps_path: str) -> List[SentenceInfo]:
    sentences:List[SentenceInfo] = []
    
    with open(timestamps_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            sentence = json.loads(line)
            sentences.append(SentenceInfo(
                sentence['time'],
                sentence['start'],
                sentence['end'],
                sentence['value']
            ))
    return sentences

def process_new_lines(sentences: List[SentenceInfo]) -> List[SentenceInfo]:
    for sentence in sentences:
        sentence.text = textwrap.fill(sentence.text, width=TEXT_CONFIG.CHARS_PER_LINE)
        sentence.lines_number = sentence.text.count('\n') + 1
    return sentences

def get_current_screen_sentences(sentences: List[SentenceInfo]) -> List[SentenceInfo]:
    current_screen_sentences = []
    current_screen_lines = 0
    for sentence in sentences:
        if current_screen_lines + sentence.lines_number <= TEXT_CONFIG.LINES_PER_SCREEN:
            current_screen_sentences.append(sentence)
            current_screen_lines += sentence.lines_number
            continue
        else:
            break
    if len(current_screen_sentences) == 0:
        current_screen_sentences.append(sentences[0])
    return current_screen_sentences

def get_filter_complex_command(timestamps_path: str, end_time: float) -> str:
    sentences = get_sentences_info(timestamps_path)
    sentences = process_new_lines(sentences)
    text_overlays = []

    sentences_used = 0
    while sentences_used < len(sentences):
        current_screen_sentences = get_current_screen_sentences(sentences[sentences_used:])
        sentences_used += len(current_screen_sentences)
        current_end_time = sentences[sentences_used].start_time / 1000 if sentences_used < len(sentences) else end_time
        current_text = '\n\n'.join([sentence.text for sentence in current_screen_sentences])

        text_overlays.append(get_text_overlay_filter(current_text, current_screen_sentences[0].start_time / 1000, current_end_time, TEXT_CONFIG.X, TEXT_CONFIG.Y))

    return ','.join(text_overlays)

def generate(configuration: GenerationConfigurationDto):
    logging.info('[Generation] Starting generation with configuration: ' + str(configuration))

    video_path = configuration.local_video_path
    voice_path = configuration.voice_path
    timestamps_path = configuration.timestamps_path

    output_path = os.path.join(tmp_dir, uuid4().hex + '.mp4')
    end_time = get_audio_duration(voice_path)

    video_end_time = convert_seconds_to_time(int(end_time) + END_TIME_OFFSET)
    ffmpeg_cmd = f"""
        {ffmpeg_path} \
        -i "{video_path}" -t {video_end_time} \
        -i "{voice_path}" -t {video_end_time} \
        -filter_complex "{get_filter_complex_command(timestamps_path, end_time)}" \
        -map 0:v -map 1:a \
        -c:a aac -c:v libx264 -preset ultrafast -crf 23 \
        "{output_path}" -shortest -y
    """
    

    logging.info('[Generation] Starting ffmpeg process with command: ' + ' '.join(ffmpeg_cmd))
    check_call(ffmpeg_cmd, shell=True)
    logging.info(f'[Generation] Ffmpeg process finished. Output file is: {output_path}')