from datetime import datetime
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from app.models.cars import CarCondition, EngineType, Transmission, CarStatus


class BaseCar(BaseModel):
    """Базовая схема авто с общими полями доменной модели."""

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    make: str
    model: str
    year: int = Field(ge=1886)
    mileage: int = Field(ge=0)
    price: float = Field(ge=0)
    condition: CarCondition
    color: str
    engine_type: EngineType
    transmission: Transmission
    status: CarStatus = CarStatus.available
    description: str | None = None


class CarCreate(BaseCar):
    vin: str = Field(min_length=3, max_length=64)


class CarRead(BaseCar):
    id: int
    vin: str
    created_at: datetime
    updated_at: datetime


class CarUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: int | None = Field(default=None, ge=1886)
    mileage: int | None = Field(default=None, ge=0)
    price: float | None = Field(default=None, ge=0)
    condition: CarCondition | None = None
    color: str | None = None
    engine_type: EngineType | None = None
    transmission: Transmission | None = None
    status: CarStatus | None = None
    description: str | None = None


class CarIdFilter(BaseModel):
    id: int


class CarListFilters(BaseModel):
    make: str | None = None
    model: str | None = None
    status: CarStatus | None = None
    engine_type: EngineType | None = None
    price_min: float | None = Field(default=None, ge=0)
    price_max: float | None = Field(default=None, ge=0)
    year_min: int | None = None
    year_max: int | None = None
    sort_by: str | None = Field(
        default=None,
        description="price|year|created_at|updated_at",
    )
    sort_dir: str | None = Field(default="desc", description="asc|desc")
