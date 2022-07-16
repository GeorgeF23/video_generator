from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
import os
from tempfile import gettempdir
from contextlib import closing
import logging

class SpeechClient():
    def __init__(self):
        self.session = Session()
        self.polly = self.session.client("polly")

    # singleton
    def get_instance():
        if not hasattr(SpeechClient, 'instance'):
            SpeechClient.instance = SpeechClient()
        return SpeechClient.instance
    
    def get_text_to_speech(self, text: str) -> str | None:
        try:
            response = self.polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Matthew")
        except (BotoCoreError, ClientError) as error:
            logging.error(f'[SpeechClient] Got an error while converting text to speech: {error}')
            return None

        # Access the audio stream from the response
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")

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
