from sqlalchemy import and_, or_
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

    @classmethod
    async def find_filtered(
        cls,
        session: AsyncSession,
        *,
        user_id: int | None = None,
        car_id: int | None = None,
        status: str | None = None,
        payment_method: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Order]:
        conditions = []
        if user_id is not None:
            conditions.append(cls.model.user_id == user_id)
        if car_id is not None:
            conditions.append(cls.model.car_id == car_id)
        if status is not None:
            conditions.append(cls.model.status == status)
        if payment_method is not None:
            conditions.append(cls.model.payment_method == payment_method)
        if q:
            pattern = f"%{q}%"
            conditions.append(
                or_(
                    cls.model.customer_name.ilike(pattern),
                    cls.model.customer_email.ilike(pattern),
                    cls.model.customer_phone.ilike(pattern),
                ),
            )

        stmt = select(cls.model)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())
