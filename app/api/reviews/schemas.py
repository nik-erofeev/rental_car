from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class BaseReview(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    customer_name: str
    user_id: int | None = Field(default=None, gt=0)
    car_id: int = Field(gt=0)
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewCreate(BaseReview):
    pass


class ReviewRead(BaseReview):
    id: int
    created_at: datetime


class ReviewUpdate(BaseModel):
    customer_name: str | None = None
    user_id: int | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class ReviewIdFilter(BaseModel):
    id: int


class ReviewDetailsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    review: "ReviewRead"
    user: Optional["ReviewUserRead"] = None
    car: "ReviewCarRead"


class ReviewUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    is_active: bool
    created_at: datetime


class ReviewCarRead(BaseModel):
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
