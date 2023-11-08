import json
import os

from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2 import service_account

load_dotenv()

project_id = os.getenv("PROJECT_ID", "")

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
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=True,
                enable_word_time_offsets=True,
            ),
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

        speech_data = []

        for result in response.results:
            print(f"Transcript: ", result)
            best_alternative = result.alternatives[0]
            for word in best_alternative.words:
                print()
                speech_data.append(
                    {
                        "start": word.start_offset,
                        "end": word.end_offset,
                        "word": word.word,
                    }
                )

        print(speech_data)

        return response
