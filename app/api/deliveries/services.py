import logging

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deliveries.exceptions import (
    DeliveryNotFoundException,
    OrderNotFoundForDeliveryException,
)

from app.api.deliveries.schemas import (
    DeliveryCreate,
    DeliveryRead,
    DeliveryUpdate,
    DeliveryIdFilter,
)
from app.dao.deliveries import DeliveriesDAO
from app.dao.orders import OrdersDAO


logger = logging.getLogger(__name__)


async def create_delivery(
    session: AsyncSession,
    data: DeliveryCreate,
) -> DeliveryRead:
    # Проверка, что заказ существует
    if not await OrdersDAO.find_one_or_none_by_id(data.order_id, session):
        raise OrderNotFoundForDeliveryException
    delivery = await DeliveriesDAO.add(session, data)
    await session.commit()
    return DeliveryRead.model_validate(delivery)


async def get_delivery(session: AsyncSession, delivery_id: int) -> DeliveryRead:
    delivery = await DeliveriesDAO.find_one_or_none_by_id(delivery_id, session)
    if not delivery:
        raise DeliveryNotFoundException
    return DeliveryRead.model_validate(delivery)


async def list_deliveries(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list[DeliveryRead]:
    page = offset // limit + 1 if limit else 1
    items = await DeliveriesDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    return [DeliveryRead.model_validate(i) for i in items]


async def update_delivery(
    session: AsyncSession,
    delivery_id: int,
    data: DeliveryUpdate,
) -> DeliveryRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_delivery(session, delivery_id)
    updated = await DeliveriesDAO.update(
        session,
        DeliveryIdFilter(id=delivery_id),
        data,
    )
    if updated == 0:
        raise DeliveryNotFoundException
    delivery = await DeliveriesDAO.find_one_or_none_by_id(delivery_id, session)
    return DeliveryRead.model_validate(delivery)


async def delete_delivery(session: AsyncSession, delivery_id: int) -> None:
    deleted = await DeliveriesDAO.delete(
        session,
        DeliveryIdFilter(id=delivery_id),
    )
    if deleted == 0:
        raise DeliveryNotFoundException
    await session.commit()
