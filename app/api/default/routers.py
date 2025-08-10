import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.default.exceptions import DatabaseNotReadyException
from app.api.default.schemas import DBResponse, PingResponse
from app.db import get_session_without_commit

router = APIRouter(
    tags=["default"],
)

logger = logging.getLogger(__name__)


@router.get(
    "/ping",
    include_in_schema=True,
    response_model=PingResponse,
    response_class=ORJSONResponse,
    summary="Проверка работоспособности сервера",
    status_code=status.HTTP_200_OK,
)
async def _ping():
    logger.debug("ping")
    return PingResponse(message="pong")


@router.get(
    "/check_database",
    include_in_schema=True,
    response_model=DBResponse,
    response_class=ORJSONResponse,
    summary="Проверка доступности базы данных",
    status_code=status.HTTP_200_OK,
)
async def _ready(session: AsyncSession = Depends(get_session_without_commit)):
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        raise DatabaseNotReadyException
    logger.info("pg ready")
    return DBResponse(status="Database is ready")
