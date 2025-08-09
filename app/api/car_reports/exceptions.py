from fastapi import HTTPException, status


CarReportNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Report not found",
)

CarNotFoundForReportException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Car not found",
)
