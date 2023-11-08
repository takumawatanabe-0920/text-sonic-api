from pydantic import BaseModel


# OK or NG
class StatusResponse(BaseModel):
    message: str
