from datetime import datetime
from enum import StrEnum, unique
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# if typing.TYPE_CHECKING:
#     from . import Pet


if TYPE_CHECKING:
    from .orders import Order
    from .reviews import Review


@unique
class UserRole(StrEnum):
    customer = "customer"
    manager = "manager"
    admin = "admin"


class User(Base):
    __tablename__: str = "users"  # type: ignore[assignment]
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="",
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
    full_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    role: Mapped[UserRole] = mapped_column(
        # SQLEnum(UserRole, name="user_role", native_enum=False),
        SQLEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.customer,
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # relations
    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="user",
    )
