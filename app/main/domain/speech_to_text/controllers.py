from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.speech_to_text.dto.response_dto import \
    SpeechToTextResponseDto
from app.main.domain.speech_to_text.services import SpeechToTextService

router = APIRouter()


@router.post("/speech_to_texts/{writing_id}", response_model=SpeechToTextResponseDto)
async def convert_to_text(
    writing_id: str,
    speech_to_text_service: Annotated[
        SpeechToTextService, Depends(SpeechToTextService)
    ],
) -> SpeechToTextResponseDto:
    return await speech_to_text_service.convert_to_text(writing_id)
