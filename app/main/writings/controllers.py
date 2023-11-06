from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.writings.dto.request_dto import CreateWritingBodyDto, UpdateWritingBodyDto
from app.main.writings.services import WritingService

from .dto.response_dto import StatusResponse, WritingResponse, WritingsResponse

router = APIRouter()


@router.get("/writings", response_model=WritingsResponse)
async def get_writings(
    writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingsResponse:
    return await writing_service.get_writings()


@router.get("/writings/{id}", response_model=WritingResponse)
async def get_writing_by_id(
    id: str, writing_service: Annotated[WritingService, Depends(WritingService)]
) -> WritingResponse:
    return await writing_service.get_writing_by_id(id)


@router.post("/writings", response_model=WritingResponse)
async def create_writing(
    reqBody: CreateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
) -> WritingResponse:
    return await writing_service.create_writing(reqBody)


@router.put("/writings/{id}", response_model=WritingResponse)
async def update_writing(
    id: str,
    reqBody: UpdateWritingBodyDto,
    writing_service: Annotated[WritingService, Depends(WritingService)],
) -> WritingResponse:
    return await writing_service.update_writing(id, reqBody)


@router.delete("/writings/{id}", response_model=StatusResponse)
async def delete_writing(
    id: str, writing_service: Annotated[WritingService, Depends(WritingService)]
) -> StatusResponse:
    return await writing_service.delete_writing(id)
