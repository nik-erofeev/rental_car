from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.config import ConfigDict

from app.api.cars.schemas import CarRead
from app.api.orders.schemas import OrderRead
from app.api.payments.schemas import PaymentRead
from app.api.reviews.schemas import ReviewRead
from app.models import UserRole


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    full_name: str | None = None
    phone: str = Field(
        ...,
        json_schema_extra={"example": "+79999999999"},
    )
    role: UserRole

    @field_validator(
        "phone",
    )
    def validate_phone(cls, v):
        # Простейшая проверка: начинается с +7 и 11 цифр
        import re

        if not re.fullmatch(r"\+7\d{10}", v):
            raise ValueError(
                "Неверный формат телефона. Используйте +7XXXXXXXXXX",
            )
        return v


class UserIdFilter(BaseModel):
    id: int


class UserUpdateDb(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    full_name: str | None = None
    phone: str | None = Field(
        None,
        json_schema_extra={"example": "+79999999999"},
    )

    @field_validator(
        "phone",
    )
    def validate_phone(cls, v):
        # Простейшая проверка: начинается с +7 и 11 цифр
        import re

        if not re.fullmatch(r"\+7\d{10}", v):
            raise ValueError(
                "Неверный формат телефона. Используйте +7XXXXXXXXXX",
            )
        return v


class UserListFilter(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


# class UserUpdate(BaseModel):
#     email: EmailStr | None = None
#     is_active: bool | None = None


class UserOrdersRead(OrderRead):
    payments: list[PaymentRead] | None = Field(default_factory=list)


class UserProfileRead(BaseModel):
    """Агрегированный профиль пользователя.

    Содержит: сам пользователь, его заказы и его отзывы.
    """

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    user: UserRead
    orders: list[UserOrdersRead]
    reviews: list[ReviewRead]
    cars: list[CarRead]
