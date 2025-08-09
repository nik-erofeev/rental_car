from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, or_

from app.dao.base import BaseDAO
from app.models.reviews import Review


class ReviewsDAO(BaseDAO[Review]):
    model = Review

    @classmethod
    async def find_by_car(
        cls,
        session: AsyncSession,
        car_id: int,
    ) -> list[Review]:
        result = await session.execute(
            select(cls.model).where(cls.model.car_id == car_id),
        )
        return list(result.scalars().all())

    @classmethod
    async def find_by_user(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> list[Review]:
        result = await session.execute(
            select(cls.model).where(cls.model.user_id == user_id),
        )
        return list(result.scalars().all())

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        review_id: int,
    ) -> Review | None:
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.user),
                selectinload(cls.model.car),
            )
            .where(cls.model.id == review_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_filtered(
        cls,
        session: AsyncSession,
        *,
        user_id: int | None = None,
        car_id: int | None = None,
        rating_min: int | None = None,
        rating_max: int | None = None,
        q: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Review]:
        conditions = []
        if user_id is not None:
            conditions.append(cls.model.user_id == user_id)
        if car_id is not None:
            conditions.append(cls.model.car_id == car_id)
        if rating_min is not None:
            conditions.append(cls.model.rating >= rating_min)
        if rating_max is not None:
            conditions.append(cls.model.rating <= rating_max)
        if q:
            pattern = f"%{q}%"
            conditions.append(
                or_(
                    cls.model.customer_name.ilike(pattern),
                    cls.model.comment.ilike(pattern),
                ),
            )

        query = select(cls.model)
        if conditions:
            query = query.where(and_(*conditions))
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())
