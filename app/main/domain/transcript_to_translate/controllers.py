from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.log.logger import logger
from app.main.domain.transcript_to_translate.dto.request_dto import (
    TranscriptToTranslateBodyDto,
)
from app.main.domain.transcript_to_translate.dto.response_dto import (
    TranscriptToTranslateResponseDto,
)
from app.main.domain.transcript_to_translate.services.services import (
    TranscriptToTranslateService,
)

router = APIRouter()


@router.post(
    "/transcript_to_translates", response_model=TranscriptToTranslateResponseDto
)
async def transcript_to_translate(
    reqBody: TranscriptToTranslateBodyDto,
    transcript_to_translate_service: Annotated[
        TranscriptToTranslateService, Depends(TranscriptToTranslateService)
    ],
) -> TranscriptToTranslateResponseDto:
    logger.info("controller.transcript_to_translate")
    return await transcript_to_translate_service.translate(reqBody.sentences)
