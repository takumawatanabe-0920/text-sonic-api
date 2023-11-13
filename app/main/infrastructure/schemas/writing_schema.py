from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WritingBase(BaseModel):
    title: str
    description: str
    user_id: Optional[str] = None


class WritingGet(BaseModel):
    id: str
    title: str
    description: str
    user_id: Optional[str] = None
    scripts: list[dict]
    script: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TranscribeSpeechWordDto(BaseModel):
    start: float
    end: float
    word: str

    class Config:
        orm_mode = True


class WritingCreate(WritingBase):
    pass


class WritingUpdate(BaseModel):
    title: str
    description: str
    scripts: list[TranscribeSpeechWordDto]
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class Writing(WritingBase):
    class Config:
        orm_mode = True
