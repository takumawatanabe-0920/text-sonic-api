from fastapi import Depends

from app.main.domain.speech_to_text.dto.response_dto import \
    SpeechToTextResponseDto
from app.main.speech_to_text.stt_client import SpeechToTextClient


class SpeechToTextService:
    def __init__(
        self,
        text_to_speech_client: SpeechToTextClient = Depends(SpeechToTextClient),
    ):
        self.text_to_speech_client = text_to_speech_client

    async def convert_to_text(self, writing_id: str) -> SpeechToTextResponseDto:
        audio_file = "audio/" + writing_id + ".mp3"
        response = self.text_to_speech_client.transcribe(audio_file)
        return SpeechToTextResponseDto(message=response)
