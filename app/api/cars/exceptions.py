from fastapi import HTTPException, status

CarNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Авто не найдено",
)

CarAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Авто с таким VIN уже существует",
)

CarsNotFoundByFiltersException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="По заданным фильтрам авто не найдены",
)

CarDeletedNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нельзя удалить авто — есть связанные заказы",
)
