import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.payments.exceptions import (
    OrderNotFoundForPaymentException,
    PaymentNotFoundException,
    PaymentsNotFoundByFiltersException,
)
from app.api.payments.schemas import (
    PaymentCreate,
    PaymentDetailsRead,
    PaymentIdFilter,
    PaymentOrderCarRead,
    PaymentOrderDeliveryRead,
    PaymentOrderRead,
    PaymentOrderUserRead,
    PaymentRead,
    PaymentUpdate,
)
from app.dao.orders import OrdersDAO
from app.dao.payments import PaymentsDAO

logger = logging.getLogger(__name__)


async def create_payment(
    session: AsyncSession,
    data: PaymentCreate,
) -> PaymentRead:
    # Проверка существования заказа
    order = await OrdersDAO.find_one_or_none_by_id(data.order_id, session)
    if not order:
        logger.warning(
            "[payments] Заказ не найден для платежа order_id=%s",
            data.order_id,
        )
        raise OrderNotFoundForPaymentException

    payment = await PaymentsDAO.add(session, data)
    await session.commit()
    logger.info("[payments] Платёж создан id=%s", payment.id)
    return PaymentRead.model_validate(payment)


async def get_payment(session: AsyncSession, payment_id: int) -> PaymentRead:
    payment = await PaymentsDAO.find_one_or_none_by_id(payment_id, session)
    if not payment:
        logger.warning("[payments] Платёж не найден id=%s", payment_id)
        raise PaymentNotFoundException
    return PaymentRead.model_validate(payment)


async def list_payments(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    order_id: int | None = None,
    status: str | None = None,
    payment_type: str | None = None,
) -> list[PaymentRead]:
    items = await PaymentsDAO.find_filtered(
        session,
        order_id=order_id,
        status=status,
        payment_type=payment_type,
        limit=limit,
        offset=offset,
    )
    if not items:
        logger.info("[payments] По фильтрам платежи не найдены")
        raise PaymentsNotFoundByFiltersException
    result = [PaymentRead.model_validate(i) for i in items]
    return result


async def update_payment(
    session: AsyncSession,
    payment_id: int,
    data: PaymentUpdate,
) -> PaymentRead:
    logger.info("[payments] Обновление платежа id=%s", payment_id)
    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[payments] Обновление без изменений id=%s", payment_id)
        return await get_payment(session, payment_id)
    updated = await PaymentsDAO.update(
        session,
        PaymentIdFilter(id=payment_id),
        data,
    )
    if updated == 0:
        logger.warning(
            "[payments] Платёж не найден для обновления id=%s",
            payment_id,
        )
        raise PaymentNotFoundException
    payment = await PaymentsDAO.find_one_or_none_by_id(payment_id, session)
    logger.info("[payments] Платёж обновлён id=%s", payment_id)
    return PaymentRead.model_validate(payment)


async def delete_payment(session: AsyncSession, payment_id: int) -> None:
    logger.info("[payments] Удаление платежа id=%s", payment_id)
    deleted = await PaymentsDAO.delete(session, PaymentIdFilter(id=payment_id))
    if deleted == 0:
        logger.warning(
            "[payments] Платёж не найден для удаления id=%s",
            payment_id,
        )
        raise PaymentNotFoundException
    await session.commit()
    logger.info("[payments] Платёж удалён id=%s", payment_id)


async def get_payment_details(
    session: AsyncSession,
    payment_id: int,
) -> PaymentDetailsRead:
    """Возвращает платеж и связанный заказ."""
    payment = await PaymentsDAO.get_with_relations(session, payment_id)
    if not payment:
        logger.warning(
            "[payments] Платёж не найден для деталей id=%s",
            payment_id,
        )
        raise PaymentNotFoundException

    order_read = PaymentOrderRead.model_validate(payment.order)
    # подставим вложенности
    order_read.user = None if payment.order.user is None else PaymentOrderUserRead.model_validate(payment.order.user)
    order_read.car = PaymentOrderCarRead.model_validate(payment.order.car)
    order_read.deliveries = [PaymentOrderDeliveryRead.model_validate(d) for d in payment.order.deliveries]

    result = PaymentDetailsRead(
        payment=PaymentRead.model_validate(payment),
        order=order_read,
    )
    return result
