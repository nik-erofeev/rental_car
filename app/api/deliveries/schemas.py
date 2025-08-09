from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from app.models.deliveries import DeliveryStatus


class BaseDelivery(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    order_id: int = Field(gt=0)
    status: DeliveryStatus
    tracking_number: str | None = None


class DeliveryCreate(BaseDelivery):
    pass


class DeliveryRead(BaseDelivery):
    id: int
    delivered_at: datetime | None
    created_at: datetime


class DeliveryUpdate(BaseModel):
    status: DeliveryStatus | None = None
    tracking_number: str | None = None


class DeliveryIdFilter(BaseModel):
    id: int


class DeliveryDetailsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    delivery: "DeliveryRead"
    order: "DeliveryOrderRead"


class DeliveryOrderRead(BaseModel):
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
    user: Optional["DeliveryOrderUserRead"] = None
    car: "DeliveryOrderCarRead"
    payments: list["DeliveryOrderPaymentRead"]


class DeliveryOrderUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_active: bool
    created_at: datetime


class DeliveryOrderCarRead(BaseModel):
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


class DeliveryOrderPaymentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    amount: float
    status: str
    payment_type: str
    transaction_id: str | None
    paid_at: datetime | None
    created_at: datetime
