from pydantic import BaseModel


class WritingBodyDto(BaseModel):
    title: str
    description: str


class WritingQueryDto(BaseModel):
    user_id: str


class CreateWritingBodyDto(WritingBodyDto):
    pass


class UpdateWritingBodyDto(WritingBodyDto):
    pass
