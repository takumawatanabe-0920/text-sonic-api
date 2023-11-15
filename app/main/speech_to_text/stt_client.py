import json
import os

from dotenv import load_dotenv
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.oauth2 import service_account

from app.core.log.logger import logger
from app.main.speech_to_text.dto.response_dto import TranscribeResponseDto
from app.main.utils.cloud_storage import CloudStorageLib, DownloadMp3BodyDto

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
        self.cloud_storage_lib = CloudStorageLib()

    def transcribe(self, audio_file) -> TranscribeResponseDto:
        logger.info("transcribe")
        print(audio_file)
        content = self.cloud_storage_lib.download_mp3_data(
            DownloadMp3BodyDto(bucket_name="text-sonic-speechs", source=audio_file)
        )

        logger.info("before RecognizeRequest")
        print(content)

        request = cloud_speech.RecognizeRequest(
            recognizer=self.recognizer,
            config=self.config,
            content=content,
        )
        # Transcribes the audio into text
        response = self.client.recognize(request=request)

        logger.info("after RecognizeRequest")

        speech_word_list = []
        audio_time = 0
        script = ""
        for result in response.results:
            best_alternative = result.alternatives[0]
            script += best_alternative.transcript
            for word in best_alternative.words:
                speech_word_list.append(
                    {
                        "start": word.start_offset.total_seconds(),  # type: ignore
                        "end": word.end_offset.total_seconds(),  # type: ignore
                        "word": word.word,
                    }
                )
            audio_time = result.result_end_offset.total_seconds()  # type: ignore

        logger.info("transcribe response")

        return TranscribeResponseDto(
            speech_word_list=speech_word_list,
            audio_time=audio_time,
            script=script,
        )
