import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.payments.schemas import (
    PaymentCreate,
    PaymentRead,
    PaymentUpdate,
    PaymentIdFilter,
    PaymentDetailsRead,
    PaymentOrderRead,
    PaymentOrderUserRead,
    PaymentOrderCarRead,
    PaymentOrderDeliveryRead,
)
from app.dao.payments import PaymentsDAO
from app.dao.orders import OrdersDAO
from app.api.payments.exceptions import (
    PaymentNotFoundException,
    OrderNotFoundForPaymentException,
)


logger = logging.getLogger(__name__)


async def create_payment(
    session: AsyncSession,
    data: PaymentCreate,
) -> PaymentRead:
    # Проверка существования заказа
    order = await OrdersDAO.find_one_or_none_by_id(data.order_id, session)
    if not order:
        raise OrderNotFoundForPaymentException

    payment = await PaymentsDAO.add(session, data)
    await session.commit()
    return PaymentRead.model_validate(payment)


async def get_payment(session: AsyncSession, payment_id: int) -> PaymentRead:
    payment = await PaymentsDAO.find_one_or_none_by_id(payment_id, session)
    if not payment:
        raise PaymentNotFoundException
    return PaymentRead.model_validate(payment)


async def list_payments(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
) -> list[PaymentRead]:
    page = offset // limit + 1 if limit else 1
    items = await PaymentsDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    return [PaymentRead.model_validate(i) for i in items]


async def update_payment(
    session: AsyncSession,
    payment_id: int,
    data: PaymentUpdate,
) -> PaymentRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_payment(session, payment_id)
    updated = await PaymentsDAO.update(
        session,
        PaymentIdFilter(id=payment_id),
        data,
    )
    if updated == 0:
        raise PaymentNotFoundException
    payment = await PaymentsDAO.find_one_or_none_by_id(payment_id, session)
    return PaymentRead.model_validate(payment)


async def delete_payment(session: AsyncSession, payment_id: int) -> None:
    deleted = await PaymentsDAO.delete(session, PaymentIdFilter(id=payment_id))
    if deleted == 0:
        raise PaymentNotFoundException
    await session.commit()


async def get_payment_details(
    session: AsyncSession,
    payment_id: int,
) -> PaymentDetailsRead:
    """Возвращает платеж и связанный заказ."""
    payment = await PaymentsDAO.get_with_relations(session, payment_id)
    if not payment:
        raise PaymentNotFoundException

    order_read = PaymentOrderRead.model_validate(payment.order)
    # подставим вложенности
    order_read.user = (
        None
        if payment.order.user is None
        else PaymentOrderUserRead.model_validate(payment.order.user)
    )
    order_read.car = PaymentOrderCarRead.model_validate(payment.order.car)
    order_read.deliveries = [
        PaymentOrderDeliveryRead.model_validate(d)
        for d in payment.order.deliveries
    ]

    return PaymentDetailsRead(
        payment=PaymentRead.model_validate(payment),
        order=order_read,
    )
