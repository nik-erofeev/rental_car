from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict

from app.models.users import UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int


class AuthRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    full_name: str | None = None
    phone: str | None = None


class AuthUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr
    is_active: bool
    role: UserRole
    created_at: datetime


class UserCreateDbAuth(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str | None = None
    phone: str | None = None


class UserFilterEmail(BaseModel):
    email: str
