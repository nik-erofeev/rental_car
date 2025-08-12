from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.schemas import AuthRegister, AuthUserRead, Token
from app.api.auth.services import (
    get_current_user,
    login_and_issue_token,
    register_user,
)
from app.core.settings import APP_CONFIG
from app.db import get_session_with_commit

router = APIRouter(prefix=f"{APP_CONFIG.api.v1}/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=AuthUserRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def register(
    data: AuthRegister,
    session: AsyncSession = Depends(get_session_with_commit),
):
    return await register_user(session, data)


@router.post(
    "/token",
    response_model=Token,
    response_class=ORJSONResponse,
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session_with_commit),
):
    return await login_and_issue_token(form_data, session)


@router.get(
    "/me",
    response_model=AuthUserRead,
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
)
async def me(current_user=Depends(get_current_user)):
    return AuthUserRead.model_validate(current_user)
