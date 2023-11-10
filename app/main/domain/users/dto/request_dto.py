from pydantic import BaseModel


class UserBodyDto(BaseModel):
    email: str
    password: str


class CreateUserBodyDto(UserBodyDto):
    pass


class UpdateUserBodyDto(UserBodyDto):
    pass
