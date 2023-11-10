from typing import Annotated

from fastapi import APIRouter, Depends

from app.main.domain.auth.dto.response_dto import LoginResponse
from app.main.domain.auth.services import AuthService
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.users.dto.request_dto import CreateUserBodyDto, UpdateUserBodyDto
from app.main.domain.users.dto.response_dto import UserResponse, UsersResponse
from app.main.domain.users.services import UserService

router = APIRouter()


@router.get("/users", response_model=UsersResponse)
async def get_users(
    user_service: Annotated[UserService, Depends(UserService)]
) -> UsersResponse:
    return user_service.get_users()


@router.get("/users/me", response_model=UserResponse)
async def get_user_by_id(
    auth_service: Annotated[AuthService, Depends(AuthService)]
) -> UserResponse:
    return auth_service.get_current_user()


@router.post("/users", response_model=LoginResponse)
async def create_user(
    reqBody: CreateUserBodyDto,
    user_service: Annotated[UserService, Depends(UserService)],
) -> LoginResponse:
    return user_service.create_user(reqBody)


@router.put("/users/{id_}", response_model=UserResponse)
async def update_user(
    id_: str,
    reqBody: UpdateUserBodyDto,
    user_service: Annotated[UserService, Depends(UserService)],
) -> UserResponse:
    return user_service.update_user(id_, reqBody)


@router.delete("/users/{id_}", response_model=StatusResponse)
async def delete_user(
    id_: str, user_service: Annotated[UserService, Depends(UserService)]
) -> StatusResponse:
    return user_service.delete_user(id_)
