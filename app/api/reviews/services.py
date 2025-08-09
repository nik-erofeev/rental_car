import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.api.reviews.exceptions import (
    ReviewNotFoundException,
    CarNotFoundForReviewException,
    UserNotFoundForReviewException,
)

from app.api.reviews.schemas import (
    ReviewCreate,
    ReviewRead,
    ReviewUpdate,
    ReviewIdFilter,
)
from app.dao.reviews import ReviewsDAO
from app.dao.cars import CarsDAO
from app.dao.users import UsersDAO


logger = logging.getLogger(__name__)


async def create_review(session: AsyncSession, data: ReviewCreate) -> ReviewRead:
    # FK проверки
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        raise CarNotFoundForReviewException
    if data.user_id is not None and not await UsersDAO.find_one_or_none_by_id(
        data.user_id, session
    ):
        raise UserNotFoundForReviewException

    review = await ReviewsDAO.add(session, data)
    await session.commit()
    return ReviewRead.model_validate(review)


async def get_review(session: AsyncSession, review_id: int) -> ReviewRead:
    review = await ReviewsDAO.find_one_or_none_by_id(review_id, session)
    if not review:
        raise ReviewNotFoundException
    return ReviewRead.model_validate(review)


async def list_reviews(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0,
    user_id: int | None = None,
    car_id: int | None = None,
) -> list[ReviewRead]:
    page = offset // limit + 1 if limit else 1
    if user_id is not None:
        items = await ReviewsDAO.find_by_user(session, user_id)
        return [ReviewRead.model_validate(i) for i in items[offset : offset + limit]]
    if car_id is not None:
        items = await ReviewsDAO.find_by_car(session, car_id)
        return [ReviewRead.model_validate(i) for i in items[offset : offset + limit]]
    items = await ReviewsDAO.paginate(session, page=page, page_size=limit, filters=None)
    return [ReviewRead.model_validate(i) for i in items]


async def update_review(
    session: AsyncSession, review_id: int, data: ReviewUpdate
) -> ReviewRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_review(session, review_id)
    updated = await ReviewsDAO.update(session, ReviewIdFilter(id=review_id), data)
    if updated == 0:
        raise ReviewNotFoundException
    review = await ReviewsDAO.find_one_or_none_by_id(review_id, session)
    return ReviewRead.model_validate(review)


async def delete_review(session: AsyncSession, review_id: int) -> None:
    deleted = await ReviewsDAO.delete(session, ReviewIdFilter(id=review_id))
    if deleted == 0:
        raise ReviewNotFoundException
    await session.commit()


