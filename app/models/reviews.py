from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .cars import Car
    from .users import User


class Review(Base):
    __tablename__: str = "reviews"  # type: ignore[assignment]
    customer_name: Mapped[str] = mapped_column(String(128), nullable=False)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    car_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cars.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    car: Mapped["Car"] = relationship("Car", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")


