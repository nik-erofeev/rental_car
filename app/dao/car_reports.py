from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.car_reports import CarReport


class CarReportsDAO(BaseDAO[CarReport]):
    model = CarReport

    @classmethod
    async def find_by_car(
        cls, session: AsyncSession, car_id: int
    ) -> list[CarReport]:
        result = await session.execute(
            select(cls.model).where(cls.model.car_id == car_id),
        )
        return list(result.scalars().all())


