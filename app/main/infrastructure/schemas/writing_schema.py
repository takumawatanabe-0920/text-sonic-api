from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class WritingBase(BaseModel):
    title: str
    description: str


class WritingGet(BaseModel):
    id: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WritingCreate(WritingBase):
    pass


class WritingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Writing(WritingBase):
    class Config:
        orm_mode = True
