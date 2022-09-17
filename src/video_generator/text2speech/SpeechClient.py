import pdb
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import os
from environment import tmp_dir
from contextlib import closing
from uuid import uuid4
import logging

class SpeechClient():
	instance = None
	def __init__(self):
		self.session = Session()
		self.polly = self.session.client("polly")
		self.engine_type = os.environ.get("POLLY_ENGINE_TYPE", "neural")
		self.voice_id = os.environ.get("POLLY_VOICE_ID", "Matthew")

	# singleton
	@staticmethod
	def get_instance():
		if not hasattr(SpeechClient, 'instance'):
			SpeechClient.instance = SpeechClient()
		return SpeechClient.instance

	def get_text_timestamps(self, text:str) -> str | None:
		try:
			response = self.polly.synthesize_speech(
				LanguageCode="en-US",
				Engine=self.engine_type,
				Text=text,
				OutputFormat="json",
				VoiceId=self.voice_id,
				SpeechMarkTypes=["sentence"]
			)
		except (BotoCoreError, ClientError) as error:
			logging.error(f'[SpeechClient] Got an error while getting sentences timestamps: {error}')
			return None
		
		if "AudioStream" in response:
			with closing(response["AudioStream"]) as stream:
				output = os.path.join(tmp_dir, uuid4().hex + ".json")

				try:
					with open(output, "wb") as file:
						file.write(stream.read())
					logging.info('[SpeechClient] Timestamps extraction successful')
					return output
				except IOError as error:
					logging.error(f'[SpeechClient] Got an error while saving timestamps file: {error}')
					return None

	def get_text_to_speech(self, text: str) -> str | None:
		try:
			response = self.polly.synthesize_speech(Engine=self.engine_type, Text=text, OutputFormat="mp3", VoiceId=self.voice_id)
		except (BotoCoreError, ClientError) as error:
			logging.error(f'[SpeechClient] Got an error while converting text to speech: {error}')
			return None

		# Access the audio stream from the response
		if "AudioStream" in response:
			with closing(response["AudioStream"]) as stream:
				output = os.path.join(tmp_dir, uuid4().hex + ".mp3")

				try:
					with open(output, "wb") as file:
						file.write(stream.read())
					logging.info('[SpeechClient] Text to speech conversion successful')
					return output
				except IOError as error:
					logging.error(f'[SpeechClient] Got an error while saving audio file: {error}')
					return None

		else:
			logging.error(f'[SpeechClient] Got an empty response')
			return None
