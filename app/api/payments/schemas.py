from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from app.models.payments import PaymentStatus, PaymentType


class BasePayment(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    order_id: int = Field(gt=0)
    amount: float = Field(ge=0)
    status: PaymentStatus
    payment_type: PaymentType
    transaction_id: str | None = None


class PaymentCreate(BasePayment):
    pass


class PaymentRead(BasePayment):
    id: int
    paid_at: datetime | None
    created_at: datetime


class PaymentDetailsRead(BaseModel):
    """Агрегированный ответ по платежу со связями."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    payment: PaymentRead
    order: "PaymentOrderRead"


class PaymentOrderRead(BaseModel):
    """Упрощённая схема заказа для деталей платежа (без циклических импортов)."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    customer_name: str
    user_id: int | None
    car_id: int
    status: str
    payment_method: str
    total_amount: float
    created_at: datetime
    updated_at: datetime
    # вложенные связи заказа
    user: Optional["PaymentOrderUserRead"] = None
    car: "PaymentOrderCarRead"
    deliveries: list["PaymentOrderDeliveryRead"]


class PaymentOrderUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_active: bool
    created_at: datetime


class PaymentOrderCarRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    vin: str
    make: str
    model: str
    year: int
    price: float
    status: str
    created_at: datetime
    updated_at: datetime


class PaymentOrderDeliveryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    status: str
    tracking_number: str | None
    delivered_at: datetime | None
    created_at: datetime


class PaymentUpdate(BaseModel):
    amount: float | None = Field(default=None, ge=0)
    status: PaymentStatus | None = None
    payment_type: PaymentType | None = None
    transaction_id: str | None = None


class PaymentIdFilter(BaseModel):
    id: int
