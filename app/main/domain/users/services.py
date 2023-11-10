from fastapi import Depends, HTTPException

from app.core.log.logger import logger
from app.main.auth.jwt import get_password_hash
from app.main.domain.auth.dto.response_dto import LoginResponse
from app.main.domain.auth.services import AuthService
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.users.dto.request_dto import CreateUserBodyDto, UpdateUserBodyDto
from app.main.domain.users.dto.response_dto import UserDto, UserResponse, UsersResponse
from app.main.infrastructure.schemas.user_schema import UserCreate, UserGet, UserUpdate
from app.main.repository.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        auth_service: AuthService = Depends(AuthService),
    ):
        self.__user_repository = user_repository
        self.__auth_service = auth_service

    async def get_users(self) -> UsersResponse:
        users = await self.__user_repository.get_all()
        return self.__convert_list_response(users)

    async def get_user(self, user_id: str) -> UserResponse:
        user = await self.__user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse(
            message=UserDto(
                id=user.id,
                email=user.email,
                encrypted_password=user.encrypted_password,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        )

    async def create_user(self, user: CreateUserBodyDto) -> LoginResponse:
        encrypted_password = get_password_hash(user.password)
        created_user = await self.__user_repository.save(
            UserCreate(email=user.email, encrypted_password=encrypted_password)
        )

        if not created_user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.__auth_service.login(user.email)

    async def update_user(self, user_id: str, user: UpdateUserBodyDto) -> UserResponse:
        updated_user = await self.__user_repository.update(
            user_id, UserUpdate(encrypted_password=user.password)
        )

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.get_user(user_id)

    async def delete_user(self, user_id: str) -> StatusResponse:
        try:
            await self.__user_repository.delete(user_id)
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")

    def __convert_list_response(self, users: list[UserGet]) -> UsersResponse:
        return UsersResponse(
            message=[
                UserDto(
                    id=user.id,
                    email=user.email,
                    encrypted_password=user.encrypted_password,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
                for user in users
            ]
        )
