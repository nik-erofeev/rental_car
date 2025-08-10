from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict

from app.api.cars.schemas import CarRead
from app.api.orders.schemas import OrderRead
from app.api.reviews.schemas import ReviewRead


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    email: EmailStr


class UserRead(UserBase):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class UserCreateDb(UserCreate):
    is_active: bool = True


class UserIdFilter(BaseModel):
    id: int


class UserUpdateDb(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserListFilter(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserProfileRead(BaseModel):
    """Агрегированный профиль пользователя.

    Содержит: сам пользователь, его заказы и его отзывы.
    """

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    user: UserRead
    orders: list[OrderRead]
    reviews: list[ReviewRead]
    cars: list[CarRead]
