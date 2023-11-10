from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    encryptedPassword: str
    email: str


class UserGet(BaseModel):
    id: str
    encryptedPassword: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    encryptedPassword: str


class User(UserBase):
    class Config:
        orm_mode = True
