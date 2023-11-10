from pydantic import BaseModel


class LoginBodyDto(BaseModel):
    email: str
