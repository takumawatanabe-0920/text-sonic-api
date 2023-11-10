from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.auth.services import AuthService
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.writings.dto.request_dto import (
    CreateWritingBodyDto,
    UpdateWritingBodyDto,
)
from app.main.domain.writings.dto.response_dto import WritingResponse, WritingsResponse
from app.main.domain.writings.services import WritingService

router = APIRouter()


@router.get("/writings", response_model=WritingsResponse)
async def get_writings(
    writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingsResponse:
    return writing_service.get_writings()


@router.get("/writings/{id_}", response_model=WritingResponse)
async def get_writing_by_id(
    id_: str, writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingResponse:
    return writing_service.get_writing_by_id(id_)


@router.post("/writings", response_model=WritingResponse)
async def create_writing(
    reqBody: CreateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> WritingResponse:
    current_user = auth_service.get_current_user()
    return writing_service.create_writing(
        CreateWritingBodyDto(**reqBody.dict(), user_id=current_user.id)
    )


@router.put("/writings/{id_}", response_model=WritingResponse)
async def update_writing(
    id_: str,
    reqBody: UpdateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> WritingResponse:
    current_user = auth_service.get_current_user()
    return writing_service.update_writing(
        id_,
        UpdateWritingBodyDto(**reqBody.dict(), user_id=current_user.id),
    )


@router.delete("/writings/{id_}", response_model=StatusResponse)
async def delete_writing(
    id_: str,
    writing_service: Annotated[WritingService, Depends(WritingService)],
    auth_service: Annotated[AuthService, Depends(AuthService)],
) -> StatusResponse:
    current_user = auth_service.get_current_user()
    return writing_service.delete_writing(id_, current_user.id)
