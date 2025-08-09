from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.orders.schemas import OrderCreate, OrderRead, OrderUpdate
from app.api.orders.services import (
    create_order,
    get_order,
    list_orders,
    update_order,
    delete_order,
)


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
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_orders(session, limit, offset)


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
