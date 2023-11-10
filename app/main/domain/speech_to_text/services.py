from typing import Annotated

from fastapi import Depends, HTTPException

from app.main.domain.speech_to_text.dto.response_dto import SpeechToTextResponseDto
from app.main.domain.writings.services import WritingService
from app.main.speech_to_text.stt_client import SpeechToTextClient


class SpeechToTextService:
    def __init__(
        self,
        text_to_speech_client: Annotated[
            SpeechToTextClient, Depends(SpeechToTextClient)
        ],
        writing_service: Annotated[WritingService, Depends(WritingService)],
    ):
        self.text_to_speech_client = text_to_speech_client
        self.writing_service = writing_service

    def convert_to_text(self, writing_id: str) -> SpeechToTextResponseDto:
        writing = self.writing_service.get_writing_by_id(writing_id)
        if not writing:
            raise HTTPException(status_code=404, detail="Writing not found")
        audio_file = "audio/" + writing_id + ".mp3"
        response = self.text_to_speech_client.transcribe(audio_file)
        return SpeechToTextResponseDto(message=response)
