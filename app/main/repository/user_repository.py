from __future__ import annotations

from prisma.types import UserUpdateInput

from app.main.infrastructure.prisma_service import prisma
from app.main.infrastructure.schemas.user_schema import UserCreate, UserGet, UserUpdate


class UserRepository:
    async def save(self, user: UserCreate) -> UserGet | None:
        created_user = await prisma.user.create(
            {
                "email": user.email,
                "encrypted_password": user.encrypted_password,
            }
        )

        return UserGet(
            id=created_user.id,
            email=created_user.email,
            encrypted_password=created_user.encrypted_password,
            created_at=created_user.created_at,
            updated_at=created_user.updated_at,
        )

    async def get_by_id(self, id_: str) -> UserGet | None:
        user = await prisma.user.find_unique(where={"id": id_})

        if not user:
            return None

        return UserGet(
            id=user.id,
            email=user.email,
            encrypted_password=user.encrypted_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_by_email(self, email: str) -> UserGet | None:
        user = await prisma.user.find_unique(where={"email": email})

        if not user:
            return None

        return UserGet(
            id=user.id,
            email=user.email,
            encrypted_password=user.encrypted_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def get_all(self) -> list[UserGet]:
        users = await prisma.user.find_many()

        return [
            UserGet(
                id=user.id,
                email=user.email,
                encrypted_password=user.encrypted_password,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            for user in users
        ]

    async def update(self, id_: str, user: UserUpdate) -> UserGet | None:
        data: UserUpdateInput = {}
        encrypted_password = user.encrypted_password

        if encrypted_password is not None:
            data["encrypted_password"] = encrypted_password

        updated_user = await prisma.user.update(
            where={"id": id_},
            data=data,
        )

        if not updated_user:
            return None

        return UserGet(
            id=updated_user.id,
            email=updated_user.email,
            encrypted_password=updated_user.encrypted_password,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
        )

    async def delete(self, id_: str) -> None:
        await prisma.user.delete(where={"id": id_})

        return None