from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.car_photos.schemas import CarPhotoCreate, CarPhotoRead, CarPhotoUpdate
from app.api.car_photos.services import (
    create_car_photo,
    get_car_photo,
    list_car_photos,
    update_car_photo,
    delete_car_photo,
)


router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/car-photos",
    tags=["car_photos"],
)


@router.post(
    "/",
    response_model=CarPhotoRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: CarPhotoCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_car_photo(session, data)


@router.get(
    "/{photo_id}",
    response_model=CarPhotoRead,
    response_class=ORJSONResponse,
)
async def get(
    photo_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_car_photo(session, photo_id)


@router.get(
    "/",
    response_model=list[CarPhotoRead],
    response_class=ORJSONResponse,
)
async def list_(
    car_id: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_car_photos(session, car_id, limit, offset)


@router.put(
    "/{photo_id}",
    response_model=CarPhotoRead,
)
async def update(
    photo_id: int,
    data: CarPhotoUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_car_photo(session, photo_id, data)


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    photo_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_car_photo(session, photo_id)
    return None


