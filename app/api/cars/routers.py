from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.cars.schemas import CarCreate, CarRead, CarUpdate
from app.api.cars.services import (
    create_car,
    get_car,
    list_cars,
    update_car,
    delete_car,
)


router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/cars",
    tags=["cars"],
)


@router.post(
    "/",
    response_model=CarRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: CarCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_car(session, data)


@router.get(
    "/{car_id}",
    response_model=CarRead,
    response_class=ORJSONResponse,
)
async def get(
    car_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_car(session, car_id)


@router.get(
    "/",
    response_model=list[CarRead],
    response_class=ORJSONResponse,
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_cars(session, limit, offset)


@router.put(
    "/{car_id}",
    response_model=CarRead,
)
async def update(
    car_id: int,
    data: CarUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_car(session, car_id, data)


@router.delete(
    "/{car_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    car_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_car(session, car_id)
    return None
