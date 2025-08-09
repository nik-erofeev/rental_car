from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.cars import Car


class CarsDAO(BaseDAO[Car]):
    model = Car

    @classmethod
    async def get_by_vin(cls, session: AsyncSession, vin: str) -> Car | None:
        result = await session.execute(
            select(cls.model).where(cls.model.vin == vin),
        )
        return result.scalar_one_or_none()
