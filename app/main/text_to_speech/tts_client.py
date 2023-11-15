import json
import os

from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

from app.core.log.logger import logger
from app.main.utils.cloud_storage import CloudStorageLib, UploadMp3BodyDto

load_dotenv()

# get credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON") or "{}"
# convert to json
credentials = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials)


class TextToSpeechClient:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)
        # voice gender ("neutral")
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        self.cloud_storage_lib = CloudStorageLib()

    async def synthesize_speech(self, text, output_filename) -> bytes:
        logger.info("synthesize_speech")
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=self.voice, audio_config=self.audio_config
        )

        await self.cloud_storage_lib.upload_mp3_data(
            UploadMp3BodyDto(
                bucket_name="text-sonic-speechs",
                destination=output_filename,
                mp3=response.audio_content,
            )
        )

        return response.audio_content
