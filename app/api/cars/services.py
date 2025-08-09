import logging
from app.api.cars.exceptions import (
    CarNotFoundException,
    CarAlreadyExistsException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cars.schemas import CarCreate, CarRead, CarUpdate, CarIdFilter
from app.dao.cars import CarsDAO


logger = logging.getLogger(__name__)


async def create_car(session: AsyncSession, data: CarCreate) -> CarRead:
    logger.info("Создание авто: %s", data)
    if await CarsDAO.get_by_vin(session, data.vin):
        # Простая проверка уникальности VIN
        raise CarAlreadyExistsException
    car = await CarsDAO.add(session, data)
    await session.commit()
    return CarRead.model_validate(car)


async def get_car(session: AsyncSession, car_id: int) -> CarRead:
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    if not car:
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
    return [CarRead.model_validate(c) for c in cars]


async def update_car(
    session: AsyncSession,
    car_id: int,
    data: CarUpdate,
) -> CarRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_car(session, car_id)
    updated = await CarsDAO.update(
        session,
        CarIdFilter(id=car_id),
        data,
    )
    if updated == 0:
        raise CarNotFoundException
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    return CarRead.model_validate(car)


async def delete_car(session: AsyncSession, car_id: int) -> None:
    deleted = await CarsDAO.delete(session, CarIdFilter(id=car_id))
    if deleted == 0:
        raise CarNotFoundException
    await session.commit()
