from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic.config import ConfigDict


class BaseCarUrl(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    url: HttpUrl

    @field_validator("url", mode="before")
    def url_to_str(cls, v):
        # Если приходит HttpUrl, преобразуем в строку
        if isinstance(v, HttpUrl):
            return str(v)
        return v


class BaseCarPhoto(BaseCarUrl):
    is_main: bool = False


class CarPhotoCreate(BaseCarPhoto):
    car_id: int = Field(gt=0)


class CarPhotoRead(BaseCarPhoto):
    id: int
    car_id: int = Field(gt=0)


class CarPhotoUpdateValue(BaseModel):
    url: HttpUrl | None = None
    is_main: bool | None = None

    @field_validator("url", mode="before")
    def url_to_str(cls, v):
        # Если приходит HttpUrl, преобразуем в строку
        if isinstance(v, HttpUrl):
            return str(v)
        return v


class CarPhotoUpdateIdFilter(BaseModel):
    id: int


class CarPhotoUpdateRequest(CarPhotoUpdateValue):
    pass


class CarPhotoGetIdFilter(BaseModel):
    car_id: int | None = None
    id: int | None = None


class CarPhotoDetailsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    photo: "CarPhotoRead"
    car: "CarPhotoCarRead"


class CarPhotoCarRead(BaseModel):
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
