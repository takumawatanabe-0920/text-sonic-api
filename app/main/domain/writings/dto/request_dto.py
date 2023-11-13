from typing import Optional
from pydantic import BaseModel

from app.main.speech_to_text.dto.response_dto import TranscribeSpeechWordDto


class WritingBodyDto(BaseModel):
    title: str
    description: str


class WritingQueryDto(BaseModel):
    user_id: str


class CreateWritingBodyDto(WritingBodyDto):
    pass


class UpdateWritingBodyDto(WritingBodyDto):
    scripts: Optional[list[TranscribeSpeechWordDto]]
