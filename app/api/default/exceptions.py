from fastapi import HTTPException, status

DatabaseNotReadyException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Database not ready",
)
