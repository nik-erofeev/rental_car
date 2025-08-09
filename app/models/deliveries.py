from enum import StrEnum, unique
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .orders import Order


@unique
class DeliveryStatus(StrEnum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    failed = "failed"


class Delivery(Base):
    __tablename__: str = "deliveries"  # type: ignore[assignment]
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[DeliveryStatus] = mapped_column(
        SQLEnum(DeliveryStatus, name="delivery_status"),
        nullable=False,
        default=DeliveryStatus.pending,
    )
    tracking_number: Mapped[str | None] = mapped_column(String(128), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    order: Mapped["Order"] = relationship("Order", back_populates="deliveries")
