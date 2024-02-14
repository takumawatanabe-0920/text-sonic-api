from pydantic import BaseModel


class ContactBodyDto(BaseModel):
    email: str
    name: str
    description: str
