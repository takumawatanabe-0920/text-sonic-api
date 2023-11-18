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
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        self.cloud_storage_lib = CloudStorageLib()

    async def synthesize_speech(
        self, text: str, output_filename: str, gender: texttospeech.SsmlVoiceGender
    ) -> bytes:
        logger.info("synthesize_speech")
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice_name = self.__get_voice_name(gender)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender[gender.name]
            or texttospeech.SsmlVoiceGender.NEUTRAL,
            name=voice_name,
        )
        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=self.audio_config
        )

        await self.cloud_storage_lib.upload_mp3_data(
            UploadMp3BodyDto(
                bucket_name="text-sonic-speechs",
                destination=output_filename,
                mp3=response.audio_content,
            )
        )

        return response.audio_content

    def __get_voice_name(self, gender: texttospeech.SsmlVoiceGender):
        if gender.name == "FEMALE":
            return "en-US-Neural2-F"

        return "en-US-Neural2-D"
