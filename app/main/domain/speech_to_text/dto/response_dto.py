from typing import Optional
from pydantic import BaseModel


class SentenceInfoDto(BaseModel):
    sentence: str
    start_time: float
    end_time: Optional[float]


class SpeechToTextDto(BaseModel):
    audio_time: float
    sentences: list[SentenceInfoDto]
    script: Optional[str]


class SpeechToTextResponseDto(BaseModel):
    message: SpeechToTextDto
