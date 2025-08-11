from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.car_photos.schemas import (
    CarPhotoCreate,
    CarPhotoRead,
    CarPhotoUpdateRequest,
)
from app.api.car_photos.services import (
    car_photo,
    create_car_photo,
    delete_car_photo,
    get_car_photo_details,
    list_car_photo,
    update_car_photo,
)
from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit

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
async def get_photo_car(
    photo_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await car_photo(session, photo_id)


@router.get(
    "/",
    response_model=list[CarPhotoRead],
    response_class=ORJSONResponse,
)
async def get_car_photos(
    car_id: int | None = None,
    id_car_photo: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_car_photo(
        session=session,
        car_id=car_id,
        id_car_photo=id_car_photo,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/{photo_id}/details",
    response_class=ORJSONResponse,
)
async def details(
    photo_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_car_photo_details(session, photo_id)


@router.put(
    "/{photo_id}",
    response_model=CarPhotoRead,
    response_class=ORJSONResponse,
    status_code=status.HTTP_201_CREATED,
)
async def update(
    photo_id: int,
    data: CarPhotoUpdateRequest,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_car_photo(session, photo_id, data)


@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete(
    photo_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_car_photo(session, photo_id)
    return {"message": "Photo deleted successfully"}
