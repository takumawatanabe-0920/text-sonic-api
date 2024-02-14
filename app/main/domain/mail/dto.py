from pydantic import BaseModel


class GmailSendMessageDTO(BaseModel):
    From: str
    Subject: str
    Message: str
