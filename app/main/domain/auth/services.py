from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status

from app.main.auth.jwt import (
    create_access_token,
    decode_access_token,
    oauth2_scheme,
    verify_password,
)
from app.main.domain.auth.dto.response_dto import LoginBase, LoginResponse
from app.main.domain.users.dto.response_dto import UserDto
from app.main.infrastructure.schemas.user_schema import UserGet
from app.main.repository.user_repository import UserRepository


class AuthService:
    def __init__(
        self,
        user_repository: Annotated[UserRepository, Depends(UserRepository)],
        token: Annotated[str, Depends(oauth2_scheme)],
    ):
        self.__user_repository = user_repository
        self.__token = token

    def login(self, email: str) -> LoginResponse:
        user = self.__user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = self.__authenticate_user(user.email, user.encrypted_password)
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

    def get_current_user(self) -> UserDto:
        user = decode_access_token(self.__token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        user = self.__user_repository.get_by_email(user["email"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return UserDto(
            id=user.id,
            email=user.email,
            encrypted_password=user.encrypted_password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def __authenticate_user(
        self, email: str, password: str
    ) -> Optional[UserGet]:  # noqa: A003
        user = self.__user_repository.get_by_email(email)
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
