from datetime import datetime

from pydantic import BaseModel


class WritingDto(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


class WritingsResponse(BaseModel):
    message: list[WritingDto]


class WritingResponse(BaseModel):
    message: WritingDto


# OK or NG
class StatusResponse(BaseModel):
    message: str
