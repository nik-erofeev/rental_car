from enum import StrEnum, unique
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, TIMESTAMP, Numeric, String, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .orders import Order


@unique
class PaymentStatus(StrEnum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


@unique
class PaymentType(StrEnum):
    full = "full"
    installment = "installment"
    deposit = "deposit"


class Payment(Base):
    __tablename__: str = "payments"  # type: ignore[assignment]
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.pending,
    )
    payment_type: Mapped[PaymentType] = mapped_column(
        SQLEnum(PaymentType, name="payment_type"),
        nullable=False,
    )
    transaction_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    paid_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )

    order: Mapped["Order"] = relationship("Order", back_populates="payments")
