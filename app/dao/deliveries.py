from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.base import BaseDAO
from app.models.deliveries import Delivery


class DeliveriesDAO(BaseDAO[Delivery]):
    model = Delivery

    @classmethod
    async def find_by_order(
        cls,
        session: AsyncSession,
        order_id: int,
    ) -> list[Delivery]:
        result = await session.execute(
            select(cls.model).where(cls.model.order_id == order_id),
        )
        return list(result.scalars().all())
