from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy import delete as __delete
from sqlalchemy import update as __update
from sqlalchemy.future import select

from app.main.infrastructure.models import User
from app.main.infrastructure.schemas.user_schema import (UserCreate, UserGet,
                                                         UserUpdate)
from app.main.infrastructure.unit_of_work import UnitOfWork


class UserRepository:
    def __init__(self, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
        self.uow = uow

    def save(self, user: UserCreate) -> UserGet:
        with self.uow as uow:
            new_user = User(**user.dict())
            uow.db.add(new_user)

        return UserGet.from_orm(new_user)

    def get_by_id(self, id_: str) -> UserGet | None:
        with self.uow as uow:
            result = uow.db.execute(select(User).filter(User.id == id_))
            user = result.scalars().first()

        if not user:
            return None

        return UserGet.from_orm(user)

    def get_by_email(self, email: str) -> UserGet | None:
        with self.uow as uow:
            result = uow.db.execute(select(User).filter(User.email == email))
            user = result.scalars().first()

        if not user:
            return None

        return UserGet.from_orm(user)

    def get_all(self) -> list[UserGet]:
        with self.uow as uow:
            result = uow.db.execute(select(User))
            users = result.scalars().all()

        return [UserGet.from_orm(user) for user in users]

    def update(self, id_: str, user: UserUpdate) -> UserGet | None:
        with self.uow as uow:
            data = user.dict(exclude_unset=True)
            uow.db.execute(__update(User).where(User.id == id_).values(**data))
            uow.db.commit()
            uow.db.refresh(user)

        return self.get_by_id(id_)

    def delete(self, id_: str) -> None:
        with self.uow as uow:
            uow.db.execute(__delete(User).where(User.id == id_))
            uow.db.commit()

        return None
