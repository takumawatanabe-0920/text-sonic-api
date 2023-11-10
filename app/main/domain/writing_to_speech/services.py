from typing import Annotated

from fastapi import Depends

from app.core.log.logger import logger
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.writings.services import WritingService
from app.main.text_to_speech.tts_client import TextToSpeechClient


class WritingToSpeechService:
    def __init__(
        self,
        writing_service: Annotated[WritingService, Depends(WritingService)],
        text_to_speech_client: Annotated[
            TextToSpeechClient, Depends(TextToSpeechClient)
        ],
    ):
        self.writing_service = writing_service
        self.text_to_speech_client = text_to_speech_client

    async def convert_to_speech(self, writing_id: str) -> StatusResponse:
        try:
            writing = self.writing_service.get_writing_by_id(writing_id)

            file_name = writing.message.id + ".mp3"
            self.text_to_speech_client.synthesize_speech(
                writing.message.description, "audio/" + file_name
            )
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")
