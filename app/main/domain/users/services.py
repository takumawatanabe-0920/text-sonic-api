from fastapi import Depends, HTTPException
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.users.dto.response_dto import UserDto, UserResponse, UsersResponse
from app.main.infrastructure.schemas.user_schema import UserCreate, UserGet, UserUpdate
from app.main.repository.user_repository import UserRepository
from app.core.log.logger import logger
from app.main.domain.users.dto.request_dto import CreateUserBodyDto, UpdateUserBodyDto


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.__user_repository = user_repository

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

    async def create_user(self, user: CreateUserBodyDto) -> UserResponse:
        created_user = await self.__user_repository.save(
            UserCreate(email=user.email, encrypted_password=user.password)
        )

        if not created_user:
            raise HTTPException(status_code=404, detail="User not found")

        return await self.get_user(created_user.id)

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
