from fastapi import HTTPException, status

ReviewNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Review not found",
)

CarNotFoundForReviewException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Car not found",
)

UserNotFoundForReviewException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found",
)


ReviewsNotFoundByFiltersException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="По заданным фильтрам отзывы не найдены",
)
