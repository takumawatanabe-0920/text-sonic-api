from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from google.cloud import texttospeech
from app.core.log.logger import logger
from app.main.auth.jwt import oauth2_scheme
from app.main.domain.auth.services import AuthService
from app.main.domain.writing_to_speech.dto.request_dto import WritingToSpeechBodyDto
from app.main.domain.writing_to_speech.services import WritingToSpeechService

router = APIRouter()


@router.post("/writing_to_speeches/{writing_id}", response_class=StreamingResponse)
async def convert_to_speech(
    writing_id: str,
    reqBody: WritingToSpeechBodyDto,
    writing_to_speech_service: Annotated[
        WritingToSpeechService, Depends(WritingToSpeechService)
    ],
    auth_service: Annotated[AuthService, Depends(AuthService)],
    __token: Annotated[str, Depends(oauth2_scheme)],
) -> StreamingResponse:
    logger.info("controller.convert_to_speech")
    auth_service.get_current_user(__token)
    return await writing_to_speech_service.convert_to_speech(writing_id, reqBody.gender)
