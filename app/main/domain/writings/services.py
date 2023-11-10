from fastapi import Depends, HTTPException

from app.core.log.logger import logger
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.writings.dto.request_dto import (
    CreateWritingBodyDto,
    UpdateWritingBodyDto,
)
from app.main.domain.writings.dto.response_dto import (
    WritingDto,
    WritingResponse,
    WritingsResponse,
)
from app.main.infrastructure.schemas.writing_schema import (
    WritingCreate,
    WritingGet,
    WritingUpdate,
)
from app.main.repository.writing_repository import WritingRepository


class WritingService:
    def __init__(
        self,
        writing_repository: WritingRepository = Depends(WritingRepository),
    ):
        self.__writing_repository = writing_repository

    async def get_writings(self) -> WritingsResponse:
        writings = await self.__writing_repository.get_all()
        return self.__convert_list_response(writings)

    async def get_writing_by_id(self, id_: str) -> WritingResponse:
        writing = await self.__writing_repository.get_by_id(id_)
        if not writing:
            raise HTTPException(status_code=404, detail="Writing not found")

        return WritingResponse(
            message=WritingDto(
                id=writing.id,
                title=writing.title,
                description=writing.description,
                created_at=writing.created_at,
                updated_at=writing.updated_at,
            )
        )

    async def create_writing(self, writing: CreateWritingBodyDto) -> WritingResponse:
        created_writing = await self.__writing_repository.save(
            WritingCreate(title=writing.title, description=writing.description)
        )
        if not created_writing:
            raise HTTPException(status_code=404, detail="Writing not found")

        return await self.get_writing_by_id(created_writing.id)

    async def update_writing(
        self, id_: str, writing: UpdateWritingBodyDto
    ) -> WritingResponse:
        updated_writing = await self.__writing_repository.update(
            id_, WritingUpdate(title=writing.title, description=writing.description)
        )

        if not updated_writing:
            raise HTTPException(status_code=404, detail="Writing not found")

        return await self.get_writing_by_id(id_)

    async def delete_writing(self, id_: str) -> StatusResponse:
        try:
            await self.__writing_repository.delete(id_)
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")

    def __convert_list_response(self, writings: list[WritingGet]) -> WritingsResponse:
        return WritingsResponse(
            message=[
                WritingDto(
                    id=writing.id,
                    title=writing.title,
                    description=writing.description,
                    created_at=writing.created_at,
                    updated_at=writing.updated_at,
                )
                for writing in writings
            ]
        )
