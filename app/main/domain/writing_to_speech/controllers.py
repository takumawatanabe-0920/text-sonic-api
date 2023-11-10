from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.writing_to_speech.services import WritingToSpeechService

router = APIRouter()


@router.post("/writing_to_speeches/{writing_id}", response_model=StatusResponse)
async def convert_to_speech(
    writing_id: str,
    writing_to_speech_service: Annotated[
        WritingToSpeechService, Depends(WritingToSpeechService)
    ],
) -> StatusResponse:
    return writing_to_speech_service.convert_to_speech(writing_id)
