from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    pass

class UserCreateDb(UserCreate):
    is_active: bool

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