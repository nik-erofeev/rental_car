from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_

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

    @classmethod
    async def find_filtered(
        cls,
        session: AsyncSession,
        *,
        order_id: int | None = None,
        status: str | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Delivery]:
        conditions = []
        if order_id is not None:
            conditions.append(cls.model.order_id == order_id)
        if status is not None:
            conditions.append(cls.model.status == status)
        if q:
            pattern = f"%{q}%"
            conditions.append(
                or_(
                    cls.model.tracking_number.ilike(pattern),
                ),
            )
        stmt = select(cls.model)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())
