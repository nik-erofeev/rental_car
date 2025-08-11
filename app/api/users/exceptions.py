from fastapi import HTTPException, status

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователь не найден",
)


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)


UserOrderException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Нельзя удалить юзера, у которого есть заказы",
)
