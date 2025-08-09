from enum import StrEnum, unique
from datetime import datetime

from sqlalchemy import String, Integer, Text, Numeric, TIMESTAMP, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


@unique
class CarCondition(StrEnum):
    new = "new"
    used = "used"


@unique
class EngineType(StrEnum):
    gasoline = "gasoline"
    diesel = "diesel"
    hybrid = "hybrid"
    electric = "electric"


@unique
class Transmission(StrEnum):
    manual = "manual"
    automatic = "automatic"
    cvt = "cvt"


@unique
class CarStatus(StrEnum):
    available = "available"
    reserved = "reserved"
    sold = "sold"


class Car(Base):
    __tablename__ = "cars"
    vin: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )
    make: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[str] = mapped_column(String(128), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    condition: Mapped[CarCondition] = mapped_column(
        SQLEnum(CarCondition, name="car_condition"),
        nullable=False,
    )
    color: Mapped[str] = mapped_column(String(64), nullable=False)
    engine_type: Mapped[EngineType] = mapped_column(
        SQLEnum(EngineType, name="engine_type"),
        nullable=False,
    )
    transmission: Mapped[Transmission] = mapped_column(
        SQLEnum(Transmission, name="transmission"),
        nullable=False,
    )
    status: Mapped[CarStatus] = mapped_column(
        SQLEnum(CarStatus, name="car_status"),
        nullable=False,
        default=CarStatus.available,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )
