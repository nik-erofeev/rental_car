from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.car_reports.schemas import (
    CarReportCreate,
    CarReportRead,
    CarReportUpdate,
)
from app.api.car_reports.services import (
    create_car_report,
    delete_car_report,
    get_car_report,
    get_car_report_details,
    list_car_reports,
    update_car_report,
)
from app.core.settings import APP_CONFIG
from app.db import get_session_without_commit

router = APIRouter(
    prefix=f"{APP_CONFIG.api.v1}/car-reports",
    tags=["car_reports"],
)


@router.post(
    "/",
    response_model=CarReportRead,
    status_code=status.HTTP_201_CREATED,
    response_class=ORJSONResponse,
)
async def create(
    data: CarReportCreate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await create_car_report(session, data)


@router.get(
    "/{report_id}",
    response_model=CarReportRead,
    response_class=ORJSONResponse,
)
async def get(
    report_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_car_report(session, report_id)


@router.get(
    "/",
    response_model=list[CarReportRead],
    response_class=ORJSONResponse,
)
async def list_(
    car_id: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await list_car_reports(session, car_id, limit, offset)


@router.get(
    "/{report_id}/details",
    response_class=ORJSONResponse,
)
async def details(
    report_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await get_car_report_details(session, report_id)


@router.put(
    "/{report_id}",
    response_model=CarReportRead,
)
async def update(
    report_id: int,
    data: CarReportUpdate,
    session: AsyncSession = Depends(get_session_without_commit),
):
    return await update_car_report(session, report_id, data)


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    report_id: int,
    session: AsyncSession = Depends(get_session_without_commit),
):
    await delete_car_report(session, report_id)
    return None
