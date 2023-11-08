from pydantic import BaseModel

from app.main.speech_to_text.dto.response_dto import TranscribeResponseDto


class SpeechToTextResponseDto(BaseModel):
    message: TranscribeResponseDto
