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
    CarPhotoDetailsRead,
    CarPhotoCarRead,
)
from app.dao.car_photos import CarPhotosDAO
from app.dao.cars import CarsDAO


logger = logging.getLogger(__name__)


async def create_car_photo(
    session: AsyncSession,
    data: CarPhotoCreate,
) -> CarPhotoRead:
    logger.info("[car_photos] Создание фото авто: %s", data)
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        logger.warning(
            "[car_photos] Авто не найдено для фото car_id=%s",
            data.car_id,
        )
        raise CarNotFoundForPhotoException
    photo = await CarPhotosDAO.add(session, data)
    await session.commit()
    logger.info("[car_photos] Фото создано id=%s", photo.id)
    return CarPhotoRead.model_validate(photo)


async def get_car_photo(session: AsyncSession, photo_id: int) -> CarPhotoRead:
    logger.info("[car_photos] Получение фото id=%s", photo_id)
    photo = await CarPhotosDAO.find_one_or_none_by_id(photo_id, session)
    if not photo:
        logger.warning("[car_photos] Фото не найдено id=%s", photo_id)
        raise CarPhotoNotFoundException
    return CarPhotoRead.model_validate(photo)


async def list_car_photos(
    session: AsyncSession,
    car_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[CarPhotoRead]:
    logger.info(
        "[car_photos] Список фото: car_id=%s limit=%s offset=%s",
        car_id,
        limit,
        offset,
    )
    if car_id is not None:
        items = await CarPhotosDAO.find_by_car(session, car_id)
        result = [
            CarPhotoRead.model_validate(i)
            for i in items[offset : offset + limit]
        ]
        logger.info("[car_photos] Найдено фото: %s", len(result))
        return result
    page = offset // limit + 1 if limit else 1
    items = await CarPhotosDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    result = [CarPhotoRead.model_validate(i) for i in items]
    logger.info("[car_photos] Найдено фото: %s", len(result))
    return result


async def update_car_photo(
    session: AsyncSession,
    photo_id: int,
    data: CarPhotoUpdate,
) -> CarPhotoRead:
    logger.info("[car_photos] Обновление фото id=%s", photo_id)
    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[car_photos] Обновление без изменений id=%s", photo_id)
        return await get_car_photo(session, photo_id)
    updated = await CarPhotosDAO.update(
        session,
        CarPhotoIdFilter(id=photo_id),
        data,
    )
    if updated == 0:
        logger.warning(
            "[car_photos] Фото не найдено для обновления id=%s",
            photo_id,
        )
        raise CarPhotoNotFoundException
    photo = await CarPhotosDAO.find_one_or_none_by_id(photo_id, session)
    logger.info("[car_photos] Фото обновлено id=%s", photo_id)
    return CarPhotoRead.model_validate(photo)


async def delete_car_photo(session: AsyncSession, photo_id: int) -> None:
    logger.info("[car_photos] Удаление фото id=%s", photo_id)
    deleted = await CarPhotosDAO.delete(session, CarPhotoIdFilter(id=photo_id))
    if deleted == 0:
        logger.warning(
            "[car_photos] Фото не найдено для удаления id=%s",
            photo_id,
        )
        raise CarPhotoNotFoundException
    await session.commit()
    logger.info("[car_photos] Фото удалено id=%s", photo_id)


async def get_car_photo_details(
    session: AsyncSession,
    photo_id: int,
) -> CarPhotoDetailsRead:
    logger.info("[car_photos] Детали фото id=%s", photo_id)
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
    logger.info("[car_photos] Детали фото собраны id=%s", photo_id)
    return result
