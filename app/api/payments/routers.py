from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.payments.schemas import (
    PaymentCreate,
    PaymentRead,
    PaymentUpdate,
    PaymentDetailsRead,
)
from app.api.payments.services import (
    create_payment,
    get_payment,
    list_payments,
    update_payment,
    delete_payment,
    get_payment_details,
)


router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/payments",
    tags=["payments"],
)


@router.post(
    "/",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: PaymentCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_payment(session, data)


@router.get(
    "/{payment_id}",
    response_model=PaymentRead,
    response_class=ORJSONResponse,
)
async def get(
    payment_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_payment(session, payment_id)


@router.get(
    "/",
    response_model=list[PaymentRead],
    response_class=ORJSONResponse,
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_payments(session, limit, offset)


@router.put(
    "/{payment_id}",
    response_model=PaymentRead,
)
async def update(
    payment_id: int,
    data: PaymentUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_payment(session, payment_id, data)


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    payment_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_payment(session, payment_id)
    return None


@router.get(
    "/{payment_id}/details",
    response_model=PaymentDetailsRead,
    response_class=ORJSONResponse,
)
async def details(
    payment_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_payment_details(session, payment_id)
