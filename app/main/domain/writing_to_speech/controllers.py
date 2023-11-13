from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.main.auth.jwt import oauth2_scheme
from app.main.domain.auth.services import AuthService
from app.main.domain.writing_to_speech.services import WritingToSpeechService

router = APIRouter()


@router.post("/writing_to_speeches/{writing_id}", response_class=FileResponse)
async def convert_to_speech(
    writing_id: str,
    writing_to_speech_service: Annotated[
        WritingToSpeechService, Depends(WritingToSpeechService)
    ],
    auth_service: Annotated[AuthService, Depends(AuthService)],
    __token: Annotated[str, Depends(oauth2_scheme)],
) -> FileResponse:
    auth_service.get_current_user(__token)
    return writing_to_speech_service.convert_to_speech(writing_id)
