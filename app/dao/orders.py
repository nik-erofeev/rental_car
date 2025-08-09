from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        order_id: int,
    ) -> Order | None:
        """Получить заказ со связанными данными.

        Включает: user, car, payments, deliveries.
        """
        stmt = (
            select(cls.model)
            .where(cls.model.id == order_id)
            .options(
                selectinload(cls.model.user),
                selectinload(cls.model.car),
                selectinload(cls.model.payments),
                selectinload(cls.model.deliveries),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
