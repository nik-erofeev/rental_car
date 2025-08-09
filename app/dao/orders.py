from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.orders import Order


class OrdersDAO(BaseDAO[Order]):
    model = Order

    @classmethod
    async def get_for_user(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> list[Order]:
        result = await session.execute(
            select(cls.model).where(cls.model.user_id == user_id),
        )
        records = list(result.scalars().all())
        return records
