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


class CarReportIdFilter(BaseModel):
    id: int
