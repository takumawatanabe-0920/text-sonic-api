from typing import Annotated
from fastapi import APIRouter, Depends

from app.main.domain.writing_to_texts.services import WritingToTextService
from app.main.domain.common.dto.response_dto import StatusResponse

router = APIRouter()


@router.get("/writing_to_texts/{writing_id}", response_model=StatusResponse)
async def convert_to_speech(
    writing_id: str,
    writing_to_text_service: Annotated[
        WritingToTextService, Depends(WritingToTextService)
    ],
) -> StatusResponse:
    return await writing_to_text_service.convert_to_speech(writing_id)
