from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
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
    full_name: str
    phone: str = Field(
        ...,
        json_schema_extra={"example": "+79999999999"},
    )

    @field_validator("phone")
    def validate_phone(cls, v):
        # Простейшая проверка: начинается с +7 и 11 цифр
        import re

        if not re.fullmatch(r"\+7\d{10}", v):
            raise ValueError(
                "Неверный формат телефона. Используйте +7XXXXXXXXXX",
            )
        return v


class AuthUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
    full_name: str
    phone: str
    role: UserRole


class UserCreateDbAuth(BaseModel):
    email: EmailStr
    hashed_password: str
    full_name: str
    phone: str


class UserFilterEmail(BaseModel):
    email: str


class UserSendKafka(BaseModel):
    email: str
    full_name: str
    phone: str
