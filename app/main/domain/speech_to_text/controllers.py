from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.log.logger import logger
from app.main.auth.jwt import oauth2_scheme
from app.main.domain.auth.services import AuthService
from app.main.domain.speech_to_text.dto.request_dto import WritingToSpeechBodyDto
from app.main.domain.speech_to_text.dto.response_dto import SpeechToTextResponseDto
from app.main.domain.speech_to_text.services.services import SpeechToTextService

router = APIRouter()


@router.post("/speech_to_texts/{writing_id}", response_model=SpeechToTextResponseDto)
async def convert_to_text(
    writing_id: str,
    reqBody: WritingToSpeechBodyDto,
    speech_to_text_service: Annotated[
        SpeechToTextService, Depends(SpeechToTextService)
    ],
    auth_service: Annotated[AuthService, Depends(AuthService)],
    __token: Annotated[str, Depends(oauth2_scheme)],
) -> SpeechToTextResponseDto:
    logger.info("controller.convert_to_text")
    auth_service.get_current_user(__token)
    return await speech_to_text_service.convert_to_text(writing_id, reqBody.gender)
