from typing import Annotated
from fastapi import APIRouter, Depends

from app.main.domain.speech_to_text.services import SpeechToTextService
from app.main.domain.common.dto.response_dto import StatusResponse

router = APIRouter()


@router.post("/speech_to_texts/{writing_id}", response_model=StatusResponse)
async def convert_to_text(
    writing_id: str,
    speech_to_text_service: Annotated[
        SpeechToTextService, Depends(SpeechToTextService)
    ],
) -> StatusResponse:
    return await speech_to_text_service.convert_to_text(writing_id)
