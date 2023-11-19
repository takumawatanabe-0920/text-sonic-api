from typing import Optional
from pydantic import BaseModel


class SentenceInfoDto(BaseModel):
    sentence: str
    start_time: float
    end_time: Optional[float]


class TranscriptToTranslateBodyDto(BaseModel):
    sentences: list[SentenceInfoDto]
    target_language: str
