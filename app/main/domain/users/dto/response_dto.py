from datetime import datetime

from pydantic import BaseModel


class UserDto(BaseModel):
    id: str
    email: str
    encryptedPassword: str
    created_at: datetime
    updated_at: datetime


class UsersResponse(BaseModel):
    message: list[UserDto]


class UserResponse(BaseModel):
    message: UserDto
