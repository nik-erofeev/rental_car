from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.models.deliveries import Delivery
from app.models.orders import Order


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

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        delivery_id: int,
    ) -> Delivery | None:
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.order).selectinload(Order.user),
                selectinload(cls.model.order).selectinload(Order.car),
                selectinload(cls.model.order).selectinload(Order.payments),
            )
            .where(cls.model.id == delivery_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
