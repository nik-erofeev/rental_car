from fastapi import HTTPException, status

DeliveryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Delivery not found",
)

OrderNotFoundForDeliveryException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Order not found",
)

DeliveriesNotFoundByFiltersException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="По заданным фильтрам доставки не найдены",
)
