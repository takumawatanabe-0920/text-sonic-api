from __future__ import annotations

from fastapi import Depends, HTTPException, status

from app.main.auth.jwt import (
    create_access_token,
    decode_access_token,
    oauth2_scheme,
    verify_password,
)
from app.main.domain.auth.dto.response_dto import LoginBase, LoginResponse
from app.main.domain.users.dto.response_dto import UserDto, UserResponse
from app.main.infrastructure.schemas.user_schema import UserGet
from app.main.repository.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.__user_repository = user_repository

    async def login(self, email: str) -> LoginResponse:
        user = await self.__user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = await self.__authenticate_user(user.email, user.encrypted_password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": user.email})

        return LoginResponse(
            message=LoginBase(access_token=access_token, token_type="bearer")
        )

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ) -> UserResponse:
        user = decode_access_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        user = await self.__user_repository.get_by_email(user["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return UserResponse(
            message=UserDto(
                id=user.id,
                email=user.email,
                encrypted_password=user.encrypted_password,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        )

    async def __authenticate_user(self, email: str, password: str) -> UserGet | None:
        user = await self.__user_repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.encrypted_password):
            return None
        return UserGet(
            id=user.id,
            email=user.email,
            encrypted_password=user.encrypted_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
