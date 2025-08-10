from sqlalchemy import and_, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

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

    @classmethod
    async def find_filtered(
        cls,
        session: AsyncSession,
        *,
        make: str | None = None,
        model: str | None = None,
        status: str | None = None,
        engine_type: str | None = None,
        price_min: float | None = None,
        price_max: float | None = None,
        year_min: int | None = None,
        year_max: int | None = None,
        sort_by: str | None = None,
        sort_dir: str | None = "desc",
        limit: int = 20,
        offset: int = 0,
    ) -> list[Car]:
        query = select(cls.model)
        conditions = []

        if make:
            conditions.append(cls.model.make == make)
        if model:
            conditions.append(cls.model.model == model)
        if status:
            # сравнение по строковому значению статуса
            conditions.append(
                cls.model.status == status,  # type: ignore[arg-type]
            )
        if engine_type:
            conditions.append(
                cls.model.engine_type == engine_type,  # type: ignore[arg-type]
            )
        if price_min is not None:
            conditions.append(cls.model.price >= price_min)
        if price_max is not None:
            conditions.append(cls.model.price <= price_max)
        if year_min is not None:
            conditions.append(cls.model.year >= year_min)
        if year_max is not None:
            conditions.append(cls.model.year <= year_max)

        if conditions:
            query = query.where(and_(*conditions))

        sort_map = {
            "price": cls.model.price,
            "year": cls.model.year,
            "created_at": cls.model.created_at,
            "updated_at": cls.model.updated_at,
        }
        if sort_by in sort_map:
            order_col = sort_map[sort_by]
            query = query.order_by(
                asc(order_col) if sort_dir == "asc" else desc(order_col),
            )

        result = await session.execute(query.offset(offset).limit(limit))
        return list(result.scalars().all())

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        car_id: int,
    ) -> Car | None:
        """Вернуть авто со связанными сущностями.

        Включает: photos, reports, reviews, orders.
        """
        stmt = (
            select(cls.model)
            .where(cls.model.id == car_id)
            .options(
                selectinload(cls.model.photos),
                selectinload(cls.model.reports),
                selectinload(cls.model.reviews),
                selectinload(cls.model.orders),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
