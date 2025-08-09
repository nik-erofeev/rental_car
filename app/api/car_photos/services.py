import logging

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.car_photos.exceptions import (
    CarPhotoNotFoundException,
    CarNotFoundForPhotoException,
)

from app.api.car_photos.schemas import (
    CarPhotoCreate,
    CarPhotoRead,
    CarPhotoUpdate,
    CarPhotoIdFilter,
)
from app.dao.car_photos import CarPhotosDAO
from app.dao.cars import CarsDAO


logger = logging.getLogger(__name__)


async def create_car_photo(
    session: AsyncSession,
    data: CarPhotoCreate,
) -> CarPhotoRead:
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        raise CarNotFoundForPhotoException
    photo = await CarPhotosDAO.add(session, data)
    await session.commit()
    return CarPhotoRead.model_validate(photo)


async def get_car_photo(session: AsyncSession, photo_id: int) -> CarPhotoRead:
    photo = await CarPhotosDAO.find_one_or_none_by_id(photo_id, session)
    if not photo:
        raise CarPhotoNotFoundException
    return CarPhotoRead.model_validate(photo)


async def list_car_photos(
    session: AsyncSession,
    car_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[CarPhotoRead]:
    if car_id is not None:
        items = await CarPhotosDAO.find_by_car(session, car_id)
        return [
            CarPhotoRead.model_validate(i)
            for i in items[offset : offset + limit]
        ]
    page = offset // limit + 1 if limit else 1
    items = await CarPhotosDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    return [CarPhotoRead.model_validate(i) for i in items]


async def update_car_photo(
    session: AsyncSession,
    photo_id: int,
    data: CarPhotoUpdate,
) -> CarPhotoRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_car_photo(session, photo_id)
    updated = await CarPhotosDAO.update(
        session,
        CarPhotoIdFilter(id=photo_id),
        data,
    )
    if updated == 0:
        raise CarPhotoNotFoundException
    photo = await CarPhotosDAO.find_one_or_none_by_id(photo_id, session)
    return CarPhotoRead.model_validate(photo)


async def delete_car_photo(session: AsyncSession, photo_id: int) -> None:
    deleted = await CarPhotosDAO.delete(session, CarPhotoIdFilter(id=photo_id))
    if deleted == 0:
        raise CarPhotoNotFoundException
    await session.commit()
