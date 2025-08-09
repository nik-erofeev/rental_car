from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic.config import ConfigDict

from app.models.orders import OrderStatus, PaymentMethod
from app.api.cars.schemas import CarRead
from app.api.payments.schemas import PaymentRead
from app.api.deliveries.schemas import DeliveryRead


class BaseOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    customer_name: str
    customer_phone: str = Field(
        ...,
        json_schema_extra={"example": "+79999999999"},
    )
    customer_email: EmailStr | None = None
    user_id: int | None = Field(default=None, gt=0)
    car_id: int = Field(gt=0)
    status: OrderStatus = OrderStatus.pending
    payment_method: PaymentMethod
    total_amount: float = Field(ge=0)
    delivery_address: str | None = None
    # delivery_date формируется сервером; из тела запроса не принимается

    @field_validator("customer_phone")
    def validate_phone(cls, v):
        # Простейшая проверка: начинается с +7 и 11 цифр
        import re

        if not re.fullmatch(r"\+7\d{10}", v):
            raise ValueError(
                "Неверный формат телефона. Используйте +7XXXXXXXXXX",
            )
        return v


class OrderCreate(BaseOrder):
    pass


class OrderRead(BaseOrder):
    id: int
    created_at: datetime
    updated_at: datetime


class OrderUpdate(BaseModel):
    customer_name: str | None = None
    customer_phone: str | None = None
    customer_email: EmailStr | None = None
    user_id: int | None = None
    status: OrderStatus | None = None
    payment_method: PaymentMethod | None = None
    total_amount: float | None = Field(default=None, ge=0)
    delivery_address: str | None = None
    # delivery_date не обновляется через API; управляется сервером

    @field_validator("customer_phone")
    def validate_phone(cls, v: str | None) -> str | None:
        # Простейшая проверка: начинается с +7 и 11 цифр
        if v is None:
            return v
        import re

        if not re.fullmatch(r"\+7\d{10}", v):
            raise ValueError(
                "Неверный формат телефона. Используйте +7XXXXXXXXXX",
            )
        return v


class OrderIdFilter(BaseModel):
    id: int


class OrderDetailsRead(BaseModel):
    """Агрегированный ответ по заказу со связями."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    order: OrderRead
    # Локальная упрощённая схема пользователя, чтобы избежать циклического импорта
    user: Optional["OrderUserRead"] = None
    car: CarRead
    payments: list[PaymentRead]
    deliveries: list[DeliveryRead]


class OrderUserRead(BaseModel):
    """Упрощённое представление пользователя в деталях заказа."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    is_active: bool
    created_at: datetime
