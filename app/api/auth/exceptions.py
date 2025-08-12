from fastapi import HTTPException, status

CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не удалось подтвердить учетные данные",
    headers={"WWW-Authenticate": "Bearer"},
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким email уже существует",
)

InvalidEmailOrPassword = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный email или пароль",
    headers={"WWW-Authenticate": "Bearer"},
)
