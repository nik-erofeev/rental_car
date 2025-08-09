from fastapi import HTTPException, status


PaymentNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Payment not found",
)

OrderNotFoundForPaymentException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Order not found",
)

PaymentsNotFoundByFiltersException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="По заданным фильтрам платежи не найдены",
)
