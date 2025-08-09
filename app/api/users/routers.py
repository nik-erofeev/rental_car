from fastapi import APIRouter, Depends, status, Query
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.users.schemas import UserCreate, UserRead, UserUpdate
from app.api.users.services import (
    example_create_user,
    example_get_user,
    example_get_users,
    example_update_user,
    example_delete_user,
)

# Публичный роутер
router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/users",
    tags=["users"],
)


@router.post(
    "/",
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя по email и паролю. Возвращает данные созданного пользователя.",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await example_create_user(session, user)


@router.get(
    "/{user_id}",
    summary="Получить пользователя по ID",
    description="Возвращает данные пользователя по его уникальному идентификатору.",
    response_model=UserRead,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await example_get_user(session, user_id)



@router.get(
    "/",
    summary="Получить список пользователей",
    description="Возвращает список пользователей с возможностью фильтрации по  статусу активности, а также с пагинацией.",
    response_model=list[UserRead],
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def get_users(
    is_active: bool | None = None,
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Максимум пользователей на страницу (1-100)",
    ),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await example_get_users(
        session=session,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Обновить пользователя",
    description="Обновляет email или статус активности пользователя по его ID. Возвращает обновлённые данные пользователя.",
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await example_update_user(session, user_id, user_update)


@router.delete(
    "/{user_id}",
    summary="Удалить пользователя",
    description="Удаляет пользователя по его ID.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await example_delete_user(session, user_id)
    return None
