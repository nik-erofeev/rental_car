import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.cars.schemas import CarRead
from app.api.reviews.schemas import ReviewRead

# связи заказы/отзывы будут загружены через UsersDAO.get_with_relations
from app.api.users.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserOrderException,
)
from app.api.users.schemas import (
    OrderUserId,
    UserCreate,
    UserCreateDb,
    UserIdFilter,
    UserListFilter,
    UserOrdersRead,
    UserProfileRead,
    UserRead,
    UserUpdateDb,
)
from app.dao.orders import OrdersDAO
from app.dao.users import UsersDAO

logger = logging.getLogger(__name__)


async def example_create_user(
    session: AsyncSession,
    user: UserCreate,
) -> UserRead:
    logger.info("[users] Создание пользователя: %s", user)
    if await UsersDAO.find_one_or_none(session=session, filters=user):
        logger.warning(
            "[users] Пользователь уже существует email=%s",
            user.email,
        )
        raise UserAlreadyExistsException

    user_db = UserCreateDb(email=user.email, is_active=True)
    user_obj = await UsersDAO.add(session=session, values=user_db)
    await session.commit()
    logger.info("[users] Пользователь создан id=%s", user_obj.id)
    return UserRead.model_validate(user_obj)


async def example_get_user(session: AsyncSession, user_id: int) -> UserRead:
    user = await UsersDAO.find_one_or_none_by_id(data_id=user_id, session=session)
    if not user:
        logger.warning("[users] Пользователь не найден id=%s", user_id)
        raise UserNotFoundException
    return UserRead.model_validate(user)


async def example_update_user(
    session: AsyncSession,
    user_id: int,
    user_update,
) -> UserRead:
    logger.info(
        "[users] Обновление пользователя id=%s данными: %s",
        user_id,
        user_update,
    )
    filter_obj = UserIdFilter(id=user_id)
    values_obj = UserUpdateDb(**user_update.model_dump(exclude_unset=True))
    updated = await UsersDAO.update(session, filter_obj, values_obj)
    if updated == 0:
        logger.warning(
            "[users] Пользователь не найден для обновления id=%s",
            user_id,
        )
        raise UserNotFoundException
    user = await UsersDAO.find_one_or_none_by_id(user_id, session)
    logger.info(
        "[users] Пользователь обновлён id=%s",
        user.id if user is not None else "unknown",
    )
    return UserRead.model_validate(user)


async def example_delete_user(session: AsyncSession, user_id: int) -> None:
    logger.info("[users] Удаление пользователя id=%s", user_id)

    filter_user_id = OrderUserId(user_id=user_id)

    user_order = await OrdersDAO.find_one_or_none(session=session, filters=filter_user_id)
    if user_order:
        logger.warning(f"Нельзя удалить юзера id: {user_id}, у которого есть заказы")
        raise UserOrderException

    filter_obj = UserIdFilter(id=user_id)
    deleted = await UsersDAO.delete(session, filter_obj)
    if deleted == 0:
        logger.warning(
            "[users] Пользователь не найден для удаления id=%s",
            user_id,
        )
        raise UserNotFoundException
    await session.commit()
    logger.info("[users] Пользователь удалён id=%s", user_id)


async def example_get_users(
    session: AsyncSession,
    is_active: bool | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[UserRead]:
    page = offset // limit + 1 if limit else 1
    filters = UserListFilter(is_active=is_active)
    users = await UsersDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=filters,
    )
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
        logger.warning(
            "[users] Пользователь не найден для профиля id=%s",
            user_id,
        )
        raise UserNotFoundException

    # Используем загруженные связи вместо дополнительных запросов
    # orders = user.orders
    # reviews = user.reviews
    cars = [o.car for o in user.orders if o.car]

    order_list = [UserOrdersRead.model_validate(order) for order in user.orders]
    result = UserProfileRead(
        user=UserRead.model_validate(user),
        orders=order_list,
        reviews=[ReviewRead.model_validate(r) for r in user.reviews],
        cars=[CarRead.model_validate(c) for c in cars],
    )

    return result
