from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

# if typing.TYPE_CHECKING:
#     from . import Pet


if TYPE_CHECKING:
    from .orders import Order
    from .reviews import Review


class User(Base):
    __tablename__: str = "users"  # type: ignore[assignment]
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
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
