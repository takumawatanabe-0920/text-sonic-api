from app.main.infrastructure.schemas.writing_schema import (
    WritingCreate,
    WritingGet,
    WritingUpdate,
)
from app.main.infrastructure.prisma_service import prisma
from typing import List, Optional
from prisma.types import WritingUpdateInput


class WritingRepository:
    async def save(self, writing: WritingCreate) -> Optional[WritingGet]:
        created_writing = await prisma.writing.create(
            {
                "title": writing.title,
                "description": writing.description,
            }
        )

        return WritingGet(
            id=created_writing.id,
            title=created_writing.title,
            description=created_writing.description,
            created_at=created_writing.created_at,
            updated_at=created_writing.updated_at,
        )

    async def get_by_id(self, id: str) -> Optional[WritingGet]:
        writing = await prisma.writing.find_unique(where={"id": id})

        if not writing:
            return None

        return WritingGet(
            id=writing.id,
            title=writing.title,
            description=writing.description,
            created_at=writing.created_at,
            updated_at=writing.updated_at,
        )

    async def get_all(self) -> List[WritingGet]:
        writings = await prisma.writing.find_many()

        return [
            WritingGet(
                id=writing.id,
                title=writing.title,
                description=writing.description,
                created_at=writing.created_at,
                updated_at=writing.updated_at,
            )
            for writing in writings
        ]

    async def update(self, id: str, writing: WritingUpdate) -> Optional[WritingGet]:
        data: WritingUpdateInput = {}
        title = writing.title
        description = writing.description

        if title is not None:
            data["title"] = title

        if description is not None:
            data["description"] = description

        updated_writing = await prisma.writing.update(
            where={"id": id},
            data=data,
        )

        if not updated_writing:
            return None

        return WritingGet(
            id=updated_writing.id,
            title=updated_writing.title,
            description=updated_writing.description,
            created_at=updated_writing.created_at,
            updated_at=updated_writing.updated_at,
        )

    async def delete(self, id: str) -> None:
        await prisma.writing.delete(where={"id": id})

        return None
