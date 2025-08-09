from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .cars import Car


class CarPhoto(Base):
    __tablename__: str = "car_photos"  # type: ignore[assignment]
    car_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    is_main: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    car: Mapped["Car"] = relationship("Car", back_populates="photos")
    
