from datetime import datetime
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
