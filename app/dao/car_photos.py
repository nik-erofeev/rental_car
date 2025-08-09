from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.car_photos import CarPhoto


class CarPhotosDAO(BaseDAO[CarPhoto]):
    model = CarPhoto

    @classmethod
    async def find_by_car(cls, session: AsyncSession, car_id: int) -> list[CarPhoto]:
        result = await session.execute(
            select(cls.model).where(cls.model.car_id == car_id),
        )
        return list(result.scalars().all())


