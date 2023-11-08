from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.writings.dto.request_dto import (
    CreateWritingBodyDto,
    UpdateWritingBodyDto,
)
from app.main.domain.writings.services import WritingService

from app.main.domain.writings.dto.response_dto import (
    WritingResponse,
    WritingsResponse,
)
from app.main.domain.common.dto.response_dto import StatusResponse

router = APIRouter()


@router.get("/writings", response_model=WritingsResponse)
async def get_writings(
    writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingsResponse:
    return await writing_service.get_writings()


@router.get("/writings/{id}", response_model=WritingResponse)
async def get_writing_by_id(
    id_: str, writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingResponse:
    return await writing_service.get_writing_by_id(id_)


@router.post("/writings", response_model=WritingResponse)
async def create_writing(
    reqBody: CreateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
) -> WritingResponse:
    return await writing_service.create_writing(reqBody)


@router.put("/writings/{id}", response_model=WritingResponse)
async def update_writing(
    id_: str,
    reqBody: UpdateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
) -> WritingResponse:
    return await writing_service.update_writing(id_, reqBody)


@router.delete("/writings/{id}", response_model=StatusResponse)
async def delete_writing(
    id_: str, writing_service: Annotated[WritingService, Depends(WritingService)]
) -> StatusResponse:
    return await writing_service.delete_writing(id_)
