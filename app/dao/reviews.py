from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.reviews import Review


class ReviewsDAO(BaseDAO[Review]):
    model = Review

    @classmethod
    async def find_by_car(cls, session: AsyncSession, car_id: int) -> list[Review]:
        result = await session.execute(
            select(cls.model).where(cls.model.car_id == car_id),
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_user(cls, session: AsyncSession, user_id: int) -> list[Review]:
        result = await session.execute(
            select(cls.model).where(cls.model.user_id == user_id),
        )
        return list(result.scalars().all())


