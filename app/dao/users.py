from app.dao.base import BaseDAO
from app.models.users import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class UsersDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> User | None:
        result = await session.execute(
            select(cls.model).where(cls.model.email == email),
        )
        return result.scalar_one_or_none()
