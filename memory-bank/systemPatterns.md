# Системные паттерны и решения

## Архитектура
- FastAPI: пул движка и async_sessionmaker хранятся в app.state (см. `app/application.py`).
- Зависимости сессии: `get_session_without_commit` / `get_session_with_commit` в `app/db.py`.
- Слои: `api` (роуты, схемы, сервисы) → `dao` (работа с БД) → `models`.

## SQLAlchemy
- Базовый класс `app.db.Base` предоставляет `id`, `created_at` и авто-`__tablename__`.
- Правило проекта: явно задаём `__tablename__` в каждой модели.
- Для Alembic все модели импортируются в `app/models/__init__.py` (autogenerate видит изменения).

## Pydantic v2
- Схемы чтения используют `model_config = {from_attributes=True}` для валидации ORM-объектов.

## Наблюдаемость
- `prometheus-fastapi-instrumentator` подключён.

## Стиль
- Предпочтительная длина строки: 120.
