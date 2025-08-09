import logging

from sqlalchemy.ext.asyncio import AsyncSession
from app.api.reviews.exceptions import (
    ReviewNotFoundException,
    CarNotFoundForReviewException,
    UserNotFoundForReviewException,
    ReviewsNotFoundByFiltersException,
)

from app.api.reviews.schemas import (
    ReviewCreate,
    ReviewRead,
    ReviewUpdate,
    ReviewIdFilter,
    ReviewDetailsRead,
    ReviewUserRead,
    ReviewCarRead,
)
from app.dao.reviews import ReviewsDAO
from app.dao.cars import CarsDAO
from app.dao.users import UsersDAO


logger = logging.getLogger(__name__)


async def create_review(
    session: AsyncSession,
    data: ReviewCreate,
) -> ReviewRead:
    # FK проверки
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        raise CarNotFoundForReviewException
    if data.user_id is not None and not await UsersDAO.find_one_or_none_by_id(
        data.user_id,
        session,
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
    rating_min: int | None = None,
    rating_max: int | None = None,
    q: str | None = None,
) -> list[ReviewRead]:
    items = await ReviewsDAO.find_filtered(
        session,
        user_id=user_id,
        car_id=car_id,
        rating_min=rating_min,
        rating_max=rating_max,
        q=q,
        limit=limit,
        offset=offset,
    )
    if not items:
        raise ReviewsNotFoundByFiltersException
    return [ReviewRead.model_validate(i) for i in items]


async def update_review(
    session: AsyncSession,
    review_id: int,
    data: ReviewUpdate,
) -> ReviewRead:
    values = data.model_dump(exclude_unset=True)
    if not values:
        return await get_review(session, review_id)
    updated = await ReviewsDAO.update(
        session,
        ReviewIdFilter(id=review_id),
        data,
    )
    if updated == 0:
        raise ReviewNotFoundException
    review = await ReviewsDAO.find_one_or_none_by_id(review_id, session)
    return ReviewRead.model_validate(review)


async def delete_review(session: AsyncSession, review_id: int) -> None:
    deleted = await ReviewsDAO.delete(session, ReviewIdFilter(id=review_id))
    if deleted == 0:
        raise ReviewNotFoundException
    await session.commit()


async def get_review_details(
    session: AsyncSession,
    review_id: int,
) -> ReviewDetailsRead:
    review = await ReviewsDAO.get_with_relations(session, review_id)
    if not review:
        raise ReviewNotFoundException

    user = review.user
    car = review.car

    return ReviewDetailsRead(
        review=ReviewRead.model_validate(review),
        user=(
            None
            if user is None
            else ReviewUserRead(
                id=user.id,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        ),
        car=ReviewCarRead(
            id=car.id,
            vin=car.vin,
            make=car.make,
            model=car.model,
            year=car.year,
            price=car.price,
            status=car.status,
            created_at=car.created_at,
            updated_at=car.updated_at,
        ),
    )
