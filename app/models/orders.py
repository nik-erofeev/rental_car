from enum import StrEnum, unique
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Text,
    TIMESTAMP,
    func,
    Numeric,
    ForeignKey,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from .cars import Car
    from .deliveries import Delivery
    from .payments import Payment
    from .users import User


@unique
class OrderStatus(StrEnum):
    pending = "pending"
    paid = "paid"
    processing = "processing"
    in_delivery = "in_delivery"
    completed = "completed"
    canceled = "canceled"


@unique
class PaymentMethod(StrEnum):
    cash = "cash"
    card = "card"
    loan = "loan"
    lease = "lease"


class Order(Base):
    __tablename__: str = "orders"  # type: ignore[assignment]
    customer_name: Mapped[str] = mapped_column(String(128), nullable=False)
    customer_phone: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_email: Mapped[str | None] = mapped_column(String(128), nullable=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    car_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cars.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.pending,
    )
    payment_method: Mapped[PaymentMethod] = mapped_column(
        SQLEnum(PaymentMethod, name="payment_method"),
        nullable=False,
    )
    total_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    delivery_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivery_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP,
        nullable=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )

    car: Mapped["Car"] = relationship("Car", back_populates="orders")
    user: Mapped["User"] = relationship("User", back_populates="orders")
    deliveries: Mapped[list["Delivery"]] = relationship(
        "Delivery",
        back_populates="order",
        cascade="all, delete-orphan",
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="order",
        cascade="all, delete-orphan",
    )
