from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

# if typing.TYPE_CHECKING:
#     from . import Pet


class User(Base):
    __tablename__ = "users"
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

    # pets: Mapped[list["Pet"]] = relationship(
    #     "Pet",
    #     back_populates="owner",
    #     # lazy='joined',
    #     # если не указаны lazy='joined' и lazy='selectin', то подгружаем
    # )
