import io
from typing import Annotated

from fastapi import Depends
from fastapi.responses import StreamingResponse

from app.core.log.logger import logger
from app.main.domain.writings.services import WritingService
from app.main.text_to_speech.tts_client import TextToSpeechClient
from app.main.utils.cloud_storage import CloudStorageLib, DownloadMp3BodyDto
from google.cloud import texttospeech


class WritingToSpeechService:
    def __init__(
        self,
        writing_service: Annotated[WritingService, Depends(WritingService)],
        text_to_speech_client: Annotated[
            TextToSpeechClient, Depends(TextToSpeechClient)
        ],
        cloud_storage_lib: Annotated[CloudStorageLib, Depends(CloudStorageLib)],
    ):
        self.writing_service = writing_service
        self.text_to_speech_client = text_to_speech_client
        self.cloud_storage_lib = cloud_storage_lib

    async def convert_to_speech(
        self,
        writing_id: str,
        gender: texttospeech.SsmlVoiceGender,
    ) -> StreamingResponse:
        logger.info("convert_to_speech")
        writing = self.writing_service.get_writing_by_id(writing_id)
        file_name = "audio/" + gender.name + "/" + writing.message.id + ".mp3"
        try:
            # bytesデータをファイルに保存して、FileResponseで返す
            mp3_data = await self.cloud_storage_lib.download_mp3_data(
                DownloadMp3BodyDto(bucket_name="text-sonic-speechs", source=file_name)
            )
            return StreamingResponse(io.BytesIO(mp3_data), media_type="audio/mpeg")

        except Exception as e:
            logger.error(e)

        audio_data = await self.text_to_speech_client.synthesize_speech(
            writing.message.description, file_name, gender
        )

        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/mpeg")
