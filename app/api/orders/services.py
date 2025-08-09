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
)
from app.dao.orders import OrdersDAO
from app.dao.cars import CarsDAO


logger = logging.getLogger(__name__)


async def create_order(session: AsyncSession, data: OrderCreate) -> OrderRead:
    # Валидация ссылок
    car = await CarsDAO.find_one_or_none_by_id(data.car_id, session)
    if not car:
        raise OrderCarNotFoundException

    # delivery_date устанавливается на стороне сервера при создании
    order = await OrdersDAO.add(session, data)
    await session.commit()
    return OrderRead.model_validate(order)


async def get_order(session: AsyncSession, order_id: int) -> OrderRead:
    order = await OrdersDAO.find_one_or_none_by_id(order_id, session)
    if not order:
        raise OrderNotFoundException
    return OrderRead.model_validate(order)


async def list_orders(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list[OrderRead]:
    page = offset // limit + 1 if limit else 1
    orders = await OrdersDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    return [OrderRead.model_validate(o) for o in orders]


async def update_order(
    session: AsyncSession,
    order_id: int,
    data: OrderUpdate,
) -> OrderRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_order(session, order_id)
    updated = await OrdersDAO.update(
        session,
        OrderIdFilter(id=order_id),
        data,
    )
    if updated == 0:
        raise OrderNotFoundException
    order = await OrdersDAO.find_one_or_none_by_id(order_id, session)
    return OrderRead.model_validate(order)


async def delete_order(session: AsyncSession, order_id: int) -> None:
    deleted = await OrdersDAO.delete(session, OrderIdFilter(id=order_id))
    if deleted == 0:
        raise OrderNotFoundException
    await session.commit()
