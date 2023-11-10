from typing import Annotated, Optional
from fastapi import Depends
from sqlalchemy.future import select
import sqlalchemy as sa
from app.main.infrastructure.models import Writing
from app.main.infrastructure.schemas.writing_schema import (
    WritingCreate,
    WritingGet,
    WritingUpdate,
)
from app.main.infrastructure.database.unit_of_work import UnitOfWork


class WritingRepository:
    def __init__(self, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
        self.uow = uow

    def save(self, writing: WritingCreate) -> WritingGet:
        with self.uow as uow:
            new_writing = Writing(**writing.dict())
            uow.db.add(new_writing)

        return WritingGet.from_orm(new_writing)

    def get_by_id(self, id_: str) -> Optional[WritingGet]:  # noqa: A003
        with self.uow as uow:
            result = uow.db.execute(select(Writing).filter(Writing.id == id_))
            writing = result.scalars().first()

        if not writing:
            return None

        return WritingGet.from_orm(writing)

    def get_all(self) -> list[WritingGet]:
        with self.uow as uow:
            result = uow.db.execute(select(Writing))
            writings = result.scalars().all()

        return [WritingGet.from_orm(writing) for writing in writings]

    def update(
        self, id_: str, writing: WritingUpdate
    ) -> Optional[WritingGet]:  # noqa: A003
        with self.uow as uow:
            data = writing.dict(exclude_unset=True)
            uow.db.execute(sa.update(Writing).where(Writing.id == id_).values(**data))
            uow.db.commit()
            updated_writing = self.get_by_id(id_)

        return updated_writing

    def delete(self, id_: str) -> None:
        with self.uow as uow:
            uow.db.execute(sa.delete(Writing).where(Writing.id == id_))
            uow.db.commit()

        return None
