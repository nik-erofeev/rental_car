import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deliveries.exceptions import (
    DeliveriesNotFoundByFiltersException,
    DeliveryNotFoundException,
    OrderNotFoundForDeliveryException,
)
from app.api.deliveries.schemas import (
    DeliveryCreate,
    DeliveryDetailsRead,
    DeliveryIdFilter,
    DeliveryOrderCarRead,
    DeliveryOrderPaymentRead,
    DeliveryOrderRead,
    DeliveryOrderUserRead,
    DeliveryRead,
    DeliveryUpdate,
)
from app.dao.deliveries import DeliveriesDAO
from app.dao.orders import OrdersDAO
from app.models.users import User

logger = logging.getLogger(__name__)


async def create_delivery(
    session: AsyncSession,
    data: DeliveryCreate,
) -> DeliveryRead:
    # Проверка, что заказ существует
    if not await OrdersDAO.find_one_or_none_by_id(data.order_id, session):
        logger.warning(
            "[deliveries] Заказ не найден для доставки order_id=%s",
            data.order_id,
        )
        raise OrderNotFoundForDeliveryException
    delivery = await DeliveriesDAO.add(session, data)
    await session.commit()
    logger.info("[deliveries] Доставка создана id=%s", delivery.id)
    return DeliveryRead.model_validate(delivery)


async def get_delivery(
    session: AsyncSession,
    delivery_id: int,
) -> DeliveryRead:
    delivery = await DeliveriesDAO.find_one_or_none_by_id(delivery_id, session)
    if not delivery:
        logger.warning("[deliveries] Доставка не найдена id=%s", delivery_id)
        raise DeliveryNotFoundException
    return DeliveryRead.model_validate(delivery)


async def list_deliveries(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    order_id: int | None = None,
    status: str | None = None,
    q: str | None = None,
) -> list[DeliveryRead]:
    items = await DeliveriesDAO.find_filtered(
        session,
        order_id=order_id,
        status=status,
        q=q,
        limit=limit,
        offset=offset,
    )
    if not items:
        logger.info("[deliveries] По фильтрам доставки не найдены")
        raise DeliveriesNotFoundByFiltersException
    result = [DeliveryRead.model_validate(i) for i in items]
    return result


async def update_delivery(
    session: AsyncSession,
    delivery_id: int,
    data: DeliveryUpdate,
) -> DeliveryRead:
    logger.info("[deliveries] Обновление доставки id=%s", delivery_id)

    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[deliveries] Обновление без изменений id=%s", delivery_id)
        return await get_delivery(session, delivery_id)
    updated = await DeliveriesDAO.update(
        session,
        DeliveryIdFilter(id=delivery_id),
        data,
    )
    if updated == 0:
        logger.warning(
            "[deliveries] Доставка не найдена для обновления id=%s",
            delivery_id,
        )
        raise DeliveryNotFoundException
    delivery = await DeliveriesDAO.find_one_or_none_by_id(delivery_id, session)
    logger.info("[deliveries] Доставка обновлена id=%s", delivery_id)
    return DeliveryRead.model_validate(delivery)


async def delete_delivery(session: AsyncSession, delivery_id: int) -> None:
    logger.info("[deliveries] Удаление доставки id=%s", delivery_id)
    deleted = await DeliveriesDAO.delete(
        session,
        DeliveryIdFilter(id=delivery_id),
    )
    if deleted == 0:
        logger.warning(
            "[deliveries] Доставка не найдена для удаления id=%s",
            delivery_id,
        )
        raise DeliveryNotFoundException
    await session.commit()
    logger.info("[deliveries] Доставка удалена id=%s", delivery_id)


async def get_delivery_details(
    session: AsyncSession,
    delivery_id: int,
) -> DeliveryDetailsRead:
    delivery = await DeliveriesDAO.get_with_relations(session, delivery_id)
    if not delivery:
        logger.warning(
            "[deliveries] Доставка не найдена для деталей id=%s",
            delivery_id,
        )
        raise DeliveryNotFoundException

    order = delivery.order

    order_user: User | None = order.user if order.user is not None else None

    result = DeliveryDetailsRead(
        delivery=DeliveryRead.model_validate(delivery),
        order=DeliveryOrderRead(
            id=order.id,
            customer_name=order.customer_name,
            user_id=order.user_id,
            car_id=order.car_id,
            status=order.status,
            payment_method=order.payment_method,
            total_amount=order.total_amount,
            created_at=order.created_at,
            updated_at=order.updated_at,
            user=(
                None
                if order_user is None
                else DeliveryOrderUserRead(
                    id=order_user.id,
                    email=order_user.email,
                    is_active=order_user.is_active,
                    created_at=order_user.created_at,
                )
            ),
            car=DeliveryOrderCarRead(
                id=order.car.id,
                vin=order.car.vin,
                make=order.car.make,
                model=order.car.model,
                year=order.car.year,
                price=order.car.price,
                status=order.car.status,
                created_at=order.car.created_at,
                updated_at=order.car.updated_at,
            ),
            payments=[
                DeliveryOrderPaymentRead(
                    id=p.id,
                    amount=p.amount,
                    status=p.status,
                    payment_type=p.payment_type,
                    transaction_id=p.transaction_id,
                    paid_at=p.paid_at,
                    created_at=p.created_at,
                )
                for p in order.payments
            ],
        ),
    )
    return result
