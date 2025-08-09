from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.models.car_photos import CarPhoto


class CarPhotosDAO(BaseDAO[CarPhoto]):
    model = CarPhoto

    @classmethod
    async def find_by_car(
        cls,
        session: AsyncSession,
        car_id: int,
    ) -> list[CarPhoto]:
        result = await session.execute(
            select(cls.model).where(cls.model.car_id == car_id),
        )
        return list(result.scalars().all())

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        photo_id: int,
    ) -> CarPhoto | None:
        query = (
            select(cls.model)
            .options(
                selectinload(cls.model.car),
            )
            .where(cls.model.id == photo_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
