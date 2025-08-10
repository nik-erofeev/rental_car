from fastapi import HTTPException, status

CarPhotoNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Photo not found",
)

CarNotFoundForPhotoException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Car not found",
)
