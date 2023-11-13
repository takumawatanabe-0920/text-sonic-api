from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WritingDto(BaseModel):
    id: str
    title: str
    description: str
    scripts: list[dict]
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class WritingsResponse(BaseModel):
    message: list[WritingDto]


class WritingResponse(BaseModel):
    message: WritingDto
