from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.orders import Order

from app.dao.base import BaseDAO
from app.models.payments import Payment


class PaymentsDAO(BaseDAO[Payment]):
    model = Payment

    @classmethod
    async def find_by_order(
        cls,
        session: AsyncSession,
        order_id: int,
    ) -> list[Payment]:
        result = await session.execute(
            select(cls.model).where(cls.model.order_id == order_id),
        )
        return list(result.scalars().all())

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        payment_id: int,
    ) -> Payment | None:
        """Возвращает платеж со связью на order."""
        stmt = (
            select(cls.model)
            .where(cls.model.id == payment_id)
            .options(
                selectinload(cls.model.order).selectinload(Order.user),
                selectinload(cls.model.order).selectinload(Order.car),
                selectinload(cls.model.order).selectinload(Order.deliveries),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
