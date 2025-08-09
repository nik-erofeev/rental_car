import logging

from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.users import UsersDAO

# связи заказы/отзывы будут загружены через UsersDAO.get_with_relations
from app.api.users.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.api.users.schemas import (
    UserCreate,
    UserCreateDb,
    UserRead,
    UserIdFilter,
    UserUpdateDb,
    UserListFilter,
    UserProfileRead,
)
from app.api.orders.schemas import OrderRead
from app.api.reviews.schemas import ReviewRead
from app.api.cars.schemas import CarRead

logger = logging.getLogger(__name__)


async def example_create_user(
    session: AsyncSession,
    user: UserCreate,
) -> UserRead:
    logger.info(f"Создание пользователя: {user}")
    if await UsersDAO.get_by_email(session, user.email):
        logger.warning(f"Пользователь с email={user.email} уже существует")
        raise UserAlreadyExistsException

    user_db = UserCreateDb(email=user.email, is_active=True)
    user_obj = await UsersDAO.add(session, user_db)
    await session.commit()
    logger.info(f"Пользователь создан: {user_obj}")
    return UserRead.model_validate(user_obj)


async def example_get_user(session: AsyncSession, user_id: int) -> UserRead:
    logger.info(f"Получение пользователя по id={user_id}")
    user = await UsersDAO.find_one_or_none_by_id(user_id, session)
    if not user:
        logger.warning(f"Пользователь с id={user_id} не найден")
        raise UserNotFoundException
    return UserRead.model_validate(user)


async def example_update_user(
    session: AsyncSession,
    user_id: int,
    user_update,
) -> UserRead:
    logger.info(f"Обновление пользователя id={user_id} данными: {user_update}")
    filter_obj = UserIdFilter(id=user_id)
    values_obj = UserUpdateDb(**user_update.model_dump(exclude_unset=True))
    updated = await UsersDAO.update(session, filter_obj, values_obj)
    if updated == 0:
        logger.warning(f"Пользователь с id={user_id} не найден для обновления")
        raise UserNotFoundException
    user = await UsersDAO.find_one_or_none_by_id(user_id, session)
    logger.info(f"Пользователь обновлён: {user}")
    return UserRead.model_validate(user)


async def example_delete_user(session: AsyncSession, user_id: int) -> None:
    logger.info(f"Удаление пользователя id={user_id}")
    filter_obj = UserIdFilter(id=user_id)
    deleted = await UsersDAO.delete(session, filter_obj)
    if deleted == 0:
        logger.warning(f"Пользователь с id={user_id} не найден для удаления")
        raise UserNotFoundException
    await session.commit()
    logger.info(f"Пользователь id={user_id} удалён")


async def example_get_users(
    session: AsyncSession,
    is_active: bool | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[UserRead]:
    logger.info(
        "Получение списка пользователей: is_active=%s, limit=%s, offset=%s",
        is_active,
        limit,
        offset,
    )
    page = offset // limit + 1 if limit else 1
    filters = UserListFilter(is_active=is_active)
    users = await UsersDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=filters,
    )
    logger.info(f"Найдено пользователей: {len(users)}")
    return [UserRead.model_validate(user) for user in users]


async def get_user_profile(
    session: AsyncSession,
    user_id: int,
) -> UserProfileRead:
    """Вернуть агрегированный профиль пользователя.

    Содержит данные пользователя, его заказы и его отзывы.
    """
    user = await UsersDAO.get_with_relations(session, user_id)
    if not user:
        raise UserNotFoundException

    # Используем загруженные связи вместо дополнительных запросов
    orders = list(user.orders)
    reviews = list(user.reviews)
    cars = [o.car for o in orders if o.car]

    return UserProfileRead(
        user=UserRead.model_validate(user),
        orders=[OrderRead.model_validate(o) for o in orders],
        reviews=[ReviewRead.model_validate(r) for r in reviews],
        cars=[CarRead.model_validate(c) for c in cars],
    )
