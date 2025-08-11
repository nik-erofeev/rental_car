from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict

from app.models.car_reports import ReportType


class BaseCarReport(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    car_id: int = Field(gt=0)
    report_type: ReportType
    data: dict


class CarReportCreate(BaseCarReport):
    pass


class CarReportRead(BaseCarReport):
    id: int


class CarReportUpdate(BaseModel):
    report_type: ReportType | None = None
    data: dict | None = None
    car_id: int | None = Field(gt=0)


class CarReportUpdateResponse(CarReportUpdate):
    id: int | None


class CarReportIdFilter(BaseModel):
    id: int | None = None
    car_id: int | None = None


class CarReportDetailsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    report: "CarReportRead"
    car: "CarReportCarRead"


class CarReportCarRead(BaseModel):
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


class CarReportPartialUpdate(BaseModel):
    id: int
    car_id: int | None = None
    report_type: ReportType | None = None
    data: dict | None = None
