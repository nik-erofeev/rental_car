from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class BaseCarPhoto(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    car_id: int = Field(gt=0)
    url: str
    is_main: bool = False


class CarPhotoCreate(BaseCarPhoto):
    pass


class CarPhotoRead(BaseCarPhoto):
    id: int


class CarPhotoUpdate(BaseModel):
    url: str | None = None
    is_main: bool | None = None


class CarPhotoIdFilter(BaseModel):
    id: int


