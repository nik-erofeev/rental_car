import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.car_photos.exceptions import (
    CarPhotoFilterNotFoundException,
    CarPhotoNotFoundException,
)
from app.api.car_photos.schemas import (
    CarPhotoCarRead,
    CarPhotoCreate,
    CarPhotoDetailsRead,
    CarPhotoGetIdFilter,
    CarPhotoRead,
    CarPhotoUpdateIdFilter,
    CarPhotoUpdateRequest,
    CarPhotoUpdateValue,
)
from app.dao.car_photos import CarPhotosDAO
from app.dao.cars import CarsDAO

logger = logging.getLogger(__name__)


async def create_car_photo(
    session: AsyncSession,
    data: CarPhotoCreate,
) -> CarPhotoRead:
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        logger.warning(
            "[car_photos] Авто не найдено для фото car_id=%s",
            data.car_id,
        )
        raise CarPhotoNotFoundException
    photo = await CarPhotosDAO.add(session, data)
    await session.commit()
    logger.info("[car_photos] Фото создано id=%s", photo.id)
    return CarPhotoRead.model_validate(photo)


async def car_photo(session: AsyncSession, photo_id: int) -> CarPhotoRead:
    photo = await CarPhotosDAO.find_one_or_none_by_id(photo_id, session)
    if not photo:
        logger.warning("[car_photos] Фото не найдено id=%s", photo_id)
        raise CarPhotoNotFoundException
    return CarPhotoRead.model_validate(photo)


async def list_car_photo(
    session: AsyncSession,
    car_id: int | None = None,
    id_car_photo: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[CarPhotoRead]:
    filter_obj = CarPhotoGetIdFilter(id=id_car_photo, car_id=car_id)
    page = offset // limit + 1 if limit else 1
    items = await CarPhotosDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=filter_obj,
    )
    if not items:
        raise CarPhotoFilterNotFoundException

    result = [CarPhotoRead.model_validate(i) for i in items]
    return result


async def update_car_photo(
    session: AsyncSession,
    photo_id: int,
    data_update: CarPhotoUpdateRequest,
) -> CarPhotoRead:
    logger.info("[car_photos] Обновление фото id=%s", photo_id)
    filter_obj = CarPhotoUpdateIdFilter(id=photo_id)
    values_obj = CarPhotoUpdateValue(**data_update.model_dump(exclude_unset=True))

    updated = await CarPhotosDAO.update(session, filter_obj, values_obj)
    if updated == 0:
        logger.warning(
            "[car_photos] Фото не найдено для обновления id=%s",
            photo_id,
        )
        raise CarPhotoNotFoundException
    await session.commit()

    updated_photo = await car_photo(session, photo_id)
    logger.info("[car_photos] Фото обновлено id=%s", photo_id)
    return updated_photo


async def delete_car_photo(session: AsyncSession, photo_id: int) -> None:
    logger.info("[car_photos] Удаление фото id=%s", photo_id)
    deleted = await CarPhotosDAO.delete(session, CarPhotoUpdateIdFilter(id=photo_id))
    if deleted == 0:
        logger.warning(
            "[car_photos] Фото не найдено для удаления id=%s",
            photo_id,
        )
        raise CarPhotoNotFoundException
    await session.commit()
    logger.info("[car_photos] Фото удалено id=%s", photo_id)
    return None


async def get_car_photo_details(
    session: AsyncSession,
    photo_id: int,
) -> CarPhotoDetailsRead:
    photo = await CarPhotosDAO.get_with_relations(session, photo_id)
    if not photo:
        logger.warning(
            "[car_photos] Фото не найдено для деталей id=%s",
            photo_id,
        )
        raise CarPhotoNotFoundException

    car = photo.car
    result = CarPhotoDetailsRead(
        photo=CarPhotoRead.model_validate(photo),
        car=CarPhotoCarRead(
            id=car.id,
            vin=car.vin,
            make=car.make,
            model=car.model,
            year=car.year,
            price=car.price,
            status=car.status,
            created_at=car.created_at,
            updated_at=car.updated_at,
        ),
    )
    return result
