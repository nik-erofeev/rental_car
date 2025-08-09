import typing

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db import Base, str_uniq

# if typing.TYPE_CHECKING:
#     from . import Pet


class User(Base):
    __tablename__ = "users"
    pass
    # email: Mapped[str_uniq] = Column(String, unique=True, index=True, nullable=False)
    # hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(nullable=False)

    # pets: Mapped[list["Pet"]] = relationship(
    #     "Pet",
    #     back_populates="owner",
    #     # lazy='joined',  # если  не указаны lazy="joined" и lazy="selectin", то подгружаем,
    # )
