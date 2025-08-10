from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deliveries.schemas import (
    DeliveryCreate,
    DeliveryRead,
    DeliveryUpdate,
)
from app.api.deliveries.services import (
    create_delivery,
    delete_delivery,
    get_delivery,
    get_delivery_details,
    list_deliveries,
    update_delivery,
)
from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.models.deliveries import DeliveryStatus

router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/deliveries",
    tags=["deliveries"],
)


@router.post(
    "/",
    response_model=DeliveryRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: DeliveryCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_delivery(session, data)


@router.get(
    "/{delivery_id}",
    response_model=DeliveryRead,
    response_class=ORJSONResponse,
)
async def get(
    delivery_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_delivery(session, delivery_id)


@router.get(
    "/",
    response_model=list[DeliveryRead],
    response_class=ORJSONResponse,
    summary="Список доставок с фильтрами",
    description=("Фильтры: order_id,\n" "status {pending|in_progress|delivered|failed},\n" "q (по tracking_number)"),
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    order_id: int | None = None,
    status: DeliveryStatus | None = None,
    q: str | None = Query(default=None, min_length=1, max_length=128),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_deliveries(
        session=session,
        limit=limit,
        offset=offset,
        order_id=order_id,
        status=(status.value if status else None),
        q=q,
    )


@router.get(
    "/{delivery_id}/details",
    response_class=ORJSONResponse,
)
async def details(
    delivery_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_delivery_details(session, delivery_id)


@router.put(
    "/{delivery_id}",
    response_model=DeliveryRead,
)
async def update(
    delivery_id: int,
    data: DeliveryUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_delivery(session, delivery_id, data)


@router.delete(
    "/{delivery_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    delivery_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_delivery(session, delivery_id)
    return None
