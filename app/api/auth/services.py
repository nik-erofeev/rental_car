import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.exceptions import (
    CredentialsException,
    InvalidEmailOrPassword,
    UserAlreadyExists,
)
from app.api.auth.schemas import (
    AuthRegister,
    AuthUserRead,
    Token,
    UserCreateDbAuth,
    UserFilterEmail,
)
from app.core.settings import APP_CONFIG
from app.dao.users import UsersDAO
from app.db import get_session_without_commit

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{APP_CONFIG.api.v1}/auth/token",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire_delta = expires_minutes or APP_CONFIG.access_token_expire_minutes
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expire_delta,
    )
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(
        payload,
        APP_CONFIG.secret_key,
        algorithm=APP_CONFIG.jwt_algorithm,
    )
    return token


async def register_user(
    session: AsyncSession,
    data: AuthRegister,
) -> AuthUserRead:
    filter_user_email = UserFilterEmail(email=str(data.email))
    # existing = await UsersDAO.get_by_email(session, str(data.email))
    existing = await UsersDAO.find_one_or_none(session=session, filters=filter_user_email)
    if existing:
        logger.warning(
            "[users] Пользователь уже существует email=%s",
            data.email,
        )
        raise UserAlreadyExists

    hashed = hash_password(data.password)

    user_payload = UserCreateDbAuth(
        email=data.email,
        hashed_password=hashed,
        full_name=data.full_name,
        phone=data.phone,
    )
    user = await UsersDAO.add(session, values=user_payload)
    # Обновим значения по умолчанию сервера (created_at и т.п.)
    await session.refresh(user)
    logger.info("[users] Пользователь создан email=%s", user.email)
    return AuthUserRead.model_validate(user)


async def authenticate_user(session: AsyncSession, email: str, password: str):
    filter_user_email = UserFilterEmail(email=email)
    user = await UsersDAO.find_one_or_none(session=session, filters=filter_user_email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def login_and_issue_token(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession,
) -> Token:
    user = await authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )
    if not user:
        raise InvalidEmailOrPassword
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session_without_commit),
):
    try:
        payload = jwt.decode(
            token,
            APP_CONFIG.secret_key,
            algorithms=[APP_CONFIG.jwt_algorithm],
        )
        subject: str | None = payload.get("sub")
        if subject is None:
            raise CredentialsException
    except JWTError:
        raise CredentialsException

    user = await UsersDAO.find_one_or_none_by_id(int(subject), session)
    if not user:
        raise CredentialsException
    return user
