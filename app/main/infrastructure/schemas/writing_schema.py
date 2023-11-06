from datetime import datetime

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
    title: str
    description: str


class Writing(WritingBase):
    class Config:
        orm_mode = True
