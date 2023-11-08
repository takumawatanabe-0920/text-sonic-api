import json
import os

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2 import service_account

project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "text-sonic-api")

# get credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON") or "{}"
# convert to json
credentials = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(credentials)


class SpeechToTextClient:
    def __init__(self):
        # Instantiates a client
        self.client = SpeechClient(credentials=credentials)
        self.config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=["en-US"],
            model="long",
        )
        self.recognizer = f"projects/{project_id}/locations/global/recognizers/_"

    def transcribe(self, audio_file):
        """Transcribe an audio file."""
        # Reads a file as bytes
        with open(audio_file, "rb") as f:
            content = f.read()

        request = cloud_speech.RecognizeRequest(
            recognizer=self.recognizer,
            config=self.config,
            content=content,
        )
        # Transcribes the audio into text
        response = self.client.recognize(request=request)

        for result in response.results:
            print(f"Transcript: {result.alternatives[0].transcript}", result)

        return response
