from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.auth.dto.request_dto import LoginBodyDto
from app.main.domain.auth.dto.response_dto import LoginResponse
from app.main.domain.auth.services import AuthService

router = APIRouter()


@router.post("/auth/login", response_model=LoginResponse)
async def login(
    reqBody: LoginBodyDto, auth_service: Annotated[AuthService, Depends(AuthService)]
) -> LoginResponse:
    return auth_service.login(reqBody)
