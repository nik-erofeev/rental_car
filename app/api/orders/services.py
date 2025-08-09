import logging
from app.api.orders.exceptions import (
    OrderNotFoundException,
    OrderCarNotFoundException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.schemas import (
    OrderCreate,
    OrderRead,
    OrderUpdate,
    OrderIdFilter,
    OrderDetailsRead,
    OrderUserRead,
)
from app.dao.orders import OrdersDAO
from app.dao.cars import CarsDAO
from app.api.orders.exceptions import OrdersNotFoundByFiltersException


logger = logging.getLogger(__name__)


async def create_order(session: AsyncSession, data: OrderCreate) -> OrderRead:
    logger.info("[orders] Создание заказа: %s", data)
    # Валидация ссылок
    car = await CarsDAO.find_one_or_none_by_id(data.car_id, session)
    if not car:
        logger.warning(
            "[orders] Авто не найдено для заказа car_id=%s",
            data.car_id,
        )
        raise OrderCarNotFoundException

    # delivery_date устанавливается на стороне сервера при создании
    order = await OrdersDAO.add(session, data)
    await session.commit()
    logger.info("[orders] Заказ создан id=%s", order.id)
    return OrderRead.model_validate(order)


async def get_order(session: AsyncSession, order_id: int) -> OrderRead:
    logger.info("[orders] Получение заказа id=%s", order_id)
    order = await OrdersDAO.find_one_or_none_by_id(order_id, session)
    if not order:
        logger.warning("[orders] Заказ не найден id=%s", order_id)
        raise OrderNotFoundException
    return OrderRead.model_validate(order)


async def list_orders(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    user_id: int | None = None,
    car_id: int | None = None,
    status: str | None = None,
    payment_method: str | None = None,
    q: str | None = None,
) -> list[OrderRead]:
    logger.info(
        "[orders] Список заказов: limit=%s offset=%s user_id=%s car_id=%s",
        limit,
        offset,
        user_id,
        car_id,
    )
    orders = await OrdersDAO.find_filtered(
        session,
        user_id=user_id,
        car_id=car_id,
        status=status,
        payment_method=payment_method,
        q=q,
        limit=limit,
        offset=offset,
    )
    if not orders:
        logger.info("[orders] По фильтрам заказы не найдены")
        raise OrdersNotFoundByFiltersException
    result = [OrderRead.model_validate(o) for o in orders]
    logger.info("[orders] Найдено заказов: %s", len(result))
    return result


async def update_order(
    session: AsyncSession,
    order_id: int,
    data: OrderUpdate,
) -> OrderRead:
    logger.info("[orders] Обновление заказа id=%s", order_id)
    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[orders] Обновление без изменений id=%s", order_id)
        return await get_order(session, order_id)
    updated = await OrdersDAO.update(
        session,
        OrderIdFilter(id=order_id),
        data,
    )
    if updated == 0:
        logger.warning(
            "[orders] Заказ не найден для обновления id=%s",
            order_id,
        )
        raise OrderNotFoundException
    order = await OrdersDAO.find_one_or_none_by_id(order_id, session)
    logger.info("[orders] Заказ обновлён id=%s", order_id)
    return OrderRead.model_validate(order)


async def delete_order(session: AsyncSession, order_id: int) -> None:
    logger.info("[orders] Удаление заказа id=%s", order_id)
    deleted = await OrdersDAO.delete(session, OrderIdFilter(id=order_id))
    if deleted == 0:
        logger.warning("[orders] Заказ не найден для удаления id=%s", order_id)
        raise OrderNotFoundException
    await session.commit()
    logger.info("[orders] Заказ удалён id=%s", order_id)


async def get_order_details(
    session: AsyncSession,
    order_id: int,
) -> OrderDetailsRead:
    """Возвращает заказ и связанные сущности.

    Включает: user, car, payments, deliveries.
    """
    logger.info("[orders] Детали заказа id=%s", order_id)
    order = await OrdersDAO.get_with_relations(session, order_id)
    if not order:
        logger.warning("[orders] Заказ не найден для деталей id=%s", order_id)
        raise OrderNotFoundException

    # Импорты схем здесь, чтобы не создавать циклы на уровне модулей
    from app.api.cars.schemas import CarRead  # noqa: WPS433
    from app.api.payments.schemas import PaymentRead  # noqa: WPS433
    from app.api.deliveries.schemas import DeliveryRead  # noqa: WPS433

    result = OrderDetailsRead(
        order=OrderRead.model_validate(order),
        user=(
            None
            if order.user is None
            else OrderUserRead.model_validate(order.user)
        ),
        car=CarRead.model_validate(order.car),
        payments=[PaymentRead.model_validate(p) for p in order.payments],
        deliveries=[DeliveryRead.model_validate(d) for d in order.deliveries],
    )
    logger.info("[orders] Детали заказа собраны id=%s", order_id)
    return result
