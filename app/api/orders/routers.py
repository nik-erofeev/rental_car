from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.orders.schemas import (
    OrderCreate,
    OrderDetailsRead,
    OrderRead,
    OrderUpdate,
)
from app.api.orders.services import (
    create_order,
    delete_order,
    get_order,
    get_order_details,
    list_orders,
    update_order,
)
from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.models.orders import OrderStatus, PaymentMethod

router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/orders",
    tags=["orders"],
)


@router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: OrderCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_order(session, data)


@router.get(
    "/{order_id}",
    response_model=OrderRead,
    response_class=ORJSONResponse,
)
async def get(
    order_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_order(session, order_id)


@router.get(
    "/",
    response_model=list[OrderRead],
    response_class=ORJSONResponse,
    summary="Список заказов с фильтрами",
    description=(
        "Фильтры: user_id, car_id,\n"
        "status {pending|paid|processing|in_delivery|completed|canceled},\n"
        "payment_method {cash|card|loan|lease}, q (по имени/почте/телефону)"
    ),
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: int | None = None,
    car_id: int | None = None,
    status: OrderStatus | None = None,
    payment_method: PaymentMethod | None = None,
    q: str | None = Query(default=None, min_length=1, max_length=128),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_orders(
        session=session,
        limit=limit,
        offset=offset,
        user_id=user_id,
        car_id=car_id,
        status=(status.value if status else None),
        payment_method=(payment_method.value if payment_method else None),
        q=q,
    )


@router.put(
    "/{order_id}",
    response_model=OrderRead,
)
async def update(
    order_id: int,
    data: OrderUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_order(session, order_id, data)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    order_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_order(session, order_id)
    return None


@router.get(
    "/{order_id}/details",
    response_model=OrderDetailsRead,
    response_class=ORJSONResponse,
)
async def details(
    order_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_order_details(session, order_id)
