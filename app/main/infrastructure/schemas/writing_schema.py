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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WritingCreate(WritingBase):
    pass


class WritingUpdate(BaseModel):
    title: str
    description: str
    user_id: Optional[str] = None


class Writing(WritingBase):
    class Config:
        orm_mode = True
