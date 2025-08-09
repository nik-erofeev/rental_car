from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    email: EmailStr


class UserRead(UserBase):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class UserCreateDb(UserCreate):
    is_active: bool = True


class UserIdFilter(BaseModel):
    id: int


class UserUpdateDb(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserListFilter(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
