import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cars.schemas import (
    CarCreate,
    CarRead,
    CarUpdate,
    CarIdFilter,
)
from app.dao.cars import CarsDAO


logger = logging.getLogger(__name__)


async def create_car(session: AsyncSession, data: CarCreate) -> CarRead:
    logger.info("Создание авто: %s", data)
    if await CarsDAO.get_by_vin(session, data.vin):
        # Простая проверка уникальности VIN
        raise ValueError("Car with this VIN already exists")
    car = await CarsDAO.add(session, data)
    await session.commit()
    return CarRead.model_validate(car)


async def get_car(session: AsyncSession, car_id: int) -> CarRead:
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    if not car:
        raise ValueError("Car not found")
    return CarRead.model_validate(car)


async def list_cars(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list[CarRead]:
    page = offset // limit + 1 if limit else 1
    cars = await CarsDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
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
        raise ValueError("Car not found")
    car = await CarsDAO.find_one_or_none_by_id(car_id, session)
    return CarRead.model_validate(car)


async def delete_car(session: AsyncSession, car_id: int) -> None:
    deleted = await CarsDAO.delete(session, CarIdFilter(id=car_id))
    if deleted == 0:
        raise ValueError("Car not found")
    await session.commit()
