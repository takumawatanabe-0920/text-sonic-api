from typing import Optional

from pydantic import BaseModel


class SentenceInfoDto(BaseModel):
    sentence: str
    start_time: float
    end_time: Optional[float]


class TranscriptToTranslateResponseDto(BaseModel):
    message: list[SentenceInfoDto]
