from fastapi import HTTPException, status

# Общие исключения для API

# Cars
CarNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Авто не найдено",
)

CarAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Авто с таким VIN уже существует",
)


# Orders
OrderNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Заказ не найден",
)

OrderCarNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Авто для указанного car_id не найдено",
)
