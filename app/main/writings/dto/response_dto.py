from datetime import datetime
from typing import List, Union
from pydantic import BaseModel


class WritingDto(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


class WritingsResponse(BaseModel):
    message: List[WritingDto]


class WritingResponse(BaseModel):
    message: Union[WritingDto, None]


# OK or NG
class StatusResponse(BaseModel):
    message: str
