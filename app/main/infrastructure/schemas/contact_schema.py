from datetime import datetime

from pydantic import BaseModel


class ContactBase(BaseModel):
    email: str
    name: str
    description: str


class ContactGet(BaseModel):
    id: str
    email: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    class Config:
        orm_mode = True
