from typing import Optional
from pydantic import BaseModel


class WritingBodyDto(BaseModel):
    title: str
    description: str
    user_id: Optional[str] = None


class CreateWritingBodyDto(WritingBodyDto):
    pass


class UpdateWritingBodyDto(WritingBodyDto):
    pass
