from fastapi import HTTPException, status

CarPhotoNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Фото не найдены",
)

CarPhotoFilterNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="По заданным фильтрам фото не найдены",
)
