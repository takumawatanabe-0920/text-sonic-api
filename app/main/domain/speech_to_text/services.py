from fastapi import Depends

from app.core.log.logger import logger
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.speech_to_text.stt_client import SpeechToTextClient


class SpeechToTextService:
    def __init__(
        self,
        text_to_speech_client: SpeechToTextClient = Depends(SpeechToTextClient),
    ):
        self.text_to_speech_client = text_to_speech_client

    async def convert_to_text(self, writing_id: str) -> StatusResponse:
        try:
            audio_file = "audio/" + writing_id + ".mp3"
            self.text_to_speech_client.transcribe(audio_file)
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")
