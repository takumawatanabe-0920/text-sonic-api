from pydantic import BaseModel


class WritingBodyDto(BaseModel):
    title: str
    description: str


class CreateWritingBodyDto(WritingBodyDto):
    pass


class UpdateWritingBodyDto(WritingBodyDto):
    pass
