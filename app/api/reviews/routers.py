from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit
from app.api.reviews.schemas import ReviewCreate, ReviewRead, ReviewUpdate
from app.api.reviews.services import (
    create_review,
    get_review,
    list_reviews,
    update_review,
    delete_review,
    get_review_details,
)


router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/reviews",
    tags=["reviews"],
)


@router.post(
    "/",
    response_model=ReviewRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: ReviewCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_review(session, data)


@router.get(
    "/{review_id}",
    response_model=ReviewRead,
    response_class=ORJSONResponse,
)
async def get(
    review_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_review(session, review_id)


@router.get(
    "/",
    response_model=list[ReviewRead],
    response_class=ORJSONResponse,
    summary="Список отзывов с фильтрами",
    description=(
        "Фильтры: user_id, car_id,\n"
        "rating_min/rating_max (1-5),\n"
        "q (по имени/комменту)"
    ),
)
async def list_(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_id: int | None = None,
    car_id: int | None = None,
    rating_min: int | None = Query(default=None, ge=1, le=5),
    rating_max: int | None = Query(default=None, ge=1, le=5),
    q: str | None = Query(default=None, min_length=1, max_length=64),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_reviews(
        session=session,
        limit=limit,
        offset=offset,
        user_id=user_id,
        car_id=car_id,
        rating_min=rating_min,
        rating_max=rating_max,
        q=q,
    )


@router.get(
    "/{review_id}/details",
    response_class=ORJSONResponse,
)
async def details(
    review_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_review_details(session, review_id)


@router.put(
    "/{review_id}",
    response_model=ReviewRead,
)
async def update(
    review_id: int,
    data: ReviewUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_review(session, review_id, data)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    review_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_review(session, review_id)
    return None
