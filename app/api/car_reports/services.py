import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.car_reports.exceptions import (
    CarNotFoundForReportException,
    CarReportNotFoundException,
)
from app.api.car_reports.schemas import (
    CarReportCarRead,
    CarReportCreate,
    CarReportDetailsRead,
    CarReportIdFilter,
    CarReportRead,
    CarReportUpdate,
)
from app.dao.car_reports import CarReportsDAO
from app.dao.cars import CarsDAO

logger = logging.getLogger(__name__)


async def create_car_report(
    session: AsyncSession,
    data: CarReportCreate,
) -> CarReportRead:
    if not await CarsDAO.find_one_or_none_by_id(data.car_id, session):
        logger.warning(
            "[car_reports] Авто не найдено для отчёта car_id=%s",
            data.car_id,
        )
        raise CarNotFoundForReportException
    report = await CarReportsDAO.add(session, data)
    await session.commit()
    return CarReportRead.model_validate(report)


async def get_car_report(
    session: AsyncSession,
    report_id: int,
) -> CarReportRead:
    report = await CarReportsDAO.find_one_or_none_by_id(report_id, session)
    if not report:
        logger.warning("[car_reports] Отчёт не найден id=%s", report_id)
        raise CarReportNotFoundException
    return CarReportRead.model_validate(report)


async def list_car_reports(
    session: AsyncSession,
    car_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[CarReportRead]:
    if car_id is not None:
        items = await CarReportsDAO.find_by_car(session, car_id)
        result = [CarReportRead.model_validate(i) for i in items[offset : offset + limit]]
        logger.info("[car_reports] Найдено отчётов: %s", len(result))
        return result
    page = offset // limit + 1 if limit else 1
    items = await CarReportsDAO.paginate(
        session,
        page=page,
        page_size=limit,
        filters=None,
    )
    result = [CarReportRead.model_validate(i) for i in items]
    return result


async def update_car_report(
    session: AsyncSession,
    report_id: int,
    data: CarReportUpdate,
) -> CarReportRead:
    logger.info("[car_reports] Обновление отчёта id=%s", report_id)
    values = data.model_dump(exclude_unset=True)
    if not values:
        logger.info("[car_reports] Обновление без изменений id=%s", report_id)
        return await get_car_report(session, report_id)
    updated = await CarReportsDAO.update(
        session,
        CarReportIdFilter(id=report_id),
        data,
    )
    if updated == 0:
        logger.warning(
            "[car_reports] Отчёт не найден для обновления id=%s",
            report_id,
        )
        raise CarReportNotFoundException
    report = await CarReportsDAO.find_one_or_none_by_id(report_id, session)
    logger.info("[car_reports] Отчёт обновлён id=%s", report_id)
    return CarReportRead.model_validate(report)


async def delete_car_report(session: AsyncSession, report_id: int) -> None:
    logger.info("[car_reports] Удаление отчёта id=%s", report_id)
    deleted = await CarReportsDAO.delete(
        session,
        CarReportIdFilter(id=report_id),
    )
    if deleted == 0:
        logger.warning(
            "[car_reports] Отчёт не найден для удаления id=%s",
            report_id,
        )
        raise CarReportNotFoundException
    await session.commit()
    logger.info("[car_reports] Отчёт удалён id=%s", report_id)


async def get_car_report_details(
    session: AsyncSession,
    report_id: int,
) -> CarReportDetailsRead:
    report = await CarReportsDAO.get_with_relations(session, report_id)
    if not report:
        logger.warning(
            "[car_reports] Отчёт не найден для деталей id=%s",
            report_id,
        )
        raise CarReportNotFoundException

    car = report.car
    result = CarReportDetailsRead(
        report=CarReportRead.model_validate(report),
        car=CarReportCarRead(
            id=car.id,
            vin=car.vin,
            make=car.make,
            model=car.model,
            year=car.year,
            price=car.price,
            status=car.status,
            created_at=car.created_at,
            updated_at=car.updated_at,
        ),
    )
    return result
