import logging
from app.api.cars.exceptions import (
    CarNotFoundException,
    CarAlreadyExistsException,
    CarsNotFoundByFiltersException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cars.schemas import (
    CarCreate,
    CarRead,
    CarUpdate,
    CarIdFilter,
    CarDetailsRead,
)
from app.dao.cars import CarsDAO
from app.api.car_photos.schemas import CarPhotoRead
from app.api.car_reports.schemas import CarReportRead
from app.api.reviews.schemas import ReviewRead
from app.api.cars.schemas import CarOrderRead


logger = logging.getLogger(__name__)


async def create_car(session: AsyncSession, data: CarCreate) -> CarRead:
    if await CarsDAO.get_by_vin(session, data.vin):
        logger.warning("[cars] VIN уже существует: %s", data.vin)
        raise CarAlreadyExistsException
    car = await CarsDAO.add(session, data)
    await session.commit()
    logger.info("[cars] Создано авто id=%s", car.id)
    return CarRead.model_validate(car)


async def get_car(session: AsyncSession, car_id: int) -> CarRead:
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    if not car:
        logger.warning("[cars] Авто не найдено id=%s", car_id)
        raise CarNotFoundException
    return CarRead.model_validate(car)


async def list_cars(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    make: str | None = None,
    model: str | None = None,
    status: str | None = None,
    engine_type: str | None = None,
    price_min: float | None = None,
    price_max: float | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    sort_by: str | None = None,
    sort_dir: str | None = "desc",
) -> list[CarRead]:
    # offset/limit используются напрямую в DAO
    cars = await CarsDAO.find_filtered(
        session,
        make=make,
        model=model,
        status=status,
        engine_type=engine_type,
        price_min=price_min,
        price_max=price_max,
        year_min=year_min,
        year_max=year_max,
        sort_by=sort_by,
        sort_dir=sort_dir,
        limit=limit,
        offset=offset,
    )
    if not cars:
        logger.info("[cars] По фильтрам авто не найдены")
        raise CarsNotFoundByFiltersException
    result = [CarRead.model_validate(c) for c in cars]
    return result


async def update_car(
    session: AsyncSession,
    car_id: int,
    data: CarUpdate,
) -> CarRead:
    logger.info("[cars] Обновление авто id=%s", car_id)
    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[cars] Обновление без изменений id=%s", car_id)
        return await get_car(session, car_id)
    updated = await CarsDAO.update(
        session,
        CarIdFilter(id=car_id),
        data,
    )
    if updated == 0:
        logger.warning("[cars] Авто не найдено для обновления id=%s", car_id)
        raise CarNotFoundException
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    logger.info("[cars] Авто обновлено id=%s", car_id)
    return CarRead.model_validate(car)


async def delete_car(session: AsyncSession, car_id: int) -> None:
    logger.info("[cars] Удаление авто id=%s", car_id)
    deleted = await CarsDAO.delete(session, CarIdFilter(id=car_id))
    if deleted == 0:
        logger.warning("[cars] Авто не найдено для удаления id=%s", car_id)
        raise CarNotFoundException
    await session.commit()
    logger.info("[cars] Авто удалено id=%s", car_id)


async def get_car_details(
    session: AsyncSession,
    car_id: int,
) -> CarDetailsRead:
    """Вернуть авто и связанные сущности: photos, reports, reviews, orders."""
    car = await CarsDAO.get_with_relations(session, car_id)
    if not car:
        logger.warning("[cars] Авто не найдено для деталей id=%s", car_id)
        raise CarNotFoundException

    details = CarDetailsRead(
        car=CarRead.model_validate(car),
        photos=[CarPhotoRead.model_validate(p) for p in car.photos],
        reports=[CarReportRead.model_validate(r) for r in car.reports],
        reviews=[ReviewRead.model_validate(rv) for rv in car.reviews],
        orders=[CarOrderRead.model_validate(o) for o in car.orders],
    )
    return details
