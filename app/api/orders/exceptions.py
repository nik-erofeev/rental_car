from fastapi import HTTPException, status


# Orders
OrderNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Заказ не найден",
)

OrderCarNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Авто для указанного car_id не найдено",
)
