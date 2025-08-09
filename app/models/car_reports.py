from enum import StrEnum, unique
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .cars import Car


@unique
class ReportType(StrEnum):
    vin_check = "vin_check"
    technical_inspection = "technical_inspection"


class CarReport(Base):
    __tablename__: str = "car_reports"  # type: ignore[assignment]
    car_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    report_type: Mapped[ReportType] = mapped_column(String(64), nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="reports")
