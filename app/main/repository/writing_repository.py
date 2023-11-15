from typing import Annotated, Optional

import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy.future import select

from app.main.infrastructure.database.unit_of_work import UnitOfWork
from app.main.infrastructure.models import Writing
from app.main.infrastructure.schemas.writing_schema import (WritingCreate,
                                                            WritingGet,
                                                            WritingUpdate)


class WritingRepository:
    def __init__(self, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
        self.uow = uow

    def save(self, writing: WritingCreate) -> WritingGet:
        with self.uow as uow:
            new_writing = Writing(**writing.dict())
            uow.db.add(new_writing)
            uow.db.commit()

            print(new_writing, "new_writing")

            return WritingGet.from_orm(new_writing)

    def get_by_id(self, id_: str) -> Optional[WritingGet]:  # noqa: A003
        with self.uow as uow:
            result = uow.db.execute(select(Writing).filter(Writing.id == id_))
            writing = result.scalars().first()

            if not writing:
                return None

            return WritingGet.from_orm(writing)

    def get_all(self, __user_id: str) -> list[WritingGet]:
        with self.uow as uow:
            result = uow.db.execute(
                select(Writing).filter(Writing.user_id == __user_id)
            )
            writings = result.scalars().all()

            return [WritingGet.from_orm(writing) for writing in writings]

    def update(
        self, id_: str, writing: WritingUpdate
    ) -> Optional[WritingGet]:  # noqa: A003
        with self.uow as uow:
            data = writing.dict(exclude_unset=True)
            uow.db.execute(
                sa.update(Writing)
                .where(Writing.id == id_)
                .values(
                    title=data["title"],
                    description=data["description"],
                    scripts=data["scripts"],
                    script=data["script"],
                )
            )
            uow.db.commit()
            updated_writing = self.get_by_id(id_)

            return updated_writing

    def delete(self, id_: str, user_id: str) -> None:
        with self.uow as uow:
            uow.db.execute(
                sa.delete(Writing)
                .where(Writing.id == id_)
                .where(Writing.user_id == user_id)
            )
            uow.db.commit()
