from pydantic import BaseModel


class LoginBase(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    message: LoginBase
