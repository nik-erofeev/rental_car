from datetime import datetime
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


class PaymentUpdate(BaseModel):
    amount: float | None = Field(default=None, ge=0)
    status: PaymentStatus | None = None
    payment_type: PaymentType | None = None
    transaction_id: str | None = None


class PaymentIdFilter(BaseModel):
    id: int
