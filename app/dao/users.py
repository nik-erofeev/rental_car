from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.models.orders import Order
from app.models.users import User


class UsersDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_by_email(
        cls,
        session: AsyncSession,
        email: str,
    ) -> User | None:
        result = await session.execute(
            select(cls.model).where(cls.model.email == email),
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_with_relations(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> User | None:
        """Получить пользователя с заказами и отзывами.

        Включает вложенные связи заказов: car, payments, deliveries.
        """
        stmt = (
            select(cls.model)
            .where(cls.model.id == user_id)
            .options(
                selectinload(cls.model.orders).selectinload(Order.car),
                selectinload(cls.model.orders).selectinload(Order.payments),
                selectinload(cls.model.orders).selectinload(Order.deliveries),
                selectinload(cls.model.reviews),
            )
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
