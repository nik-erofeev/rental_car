# Технический контекст

## Зависимости
- Python 3.12
- FastAPI, SQLAlchemy 2.0 (async), Alembic, asyncpg, Pydantic v2, pydantic-settings, Uvicorn.

## Настройки
- `app/core/settings.py` с `env_nested_delimiter="__"`.
- DSN БД: `postgresql+asyncpg://user:pass@host:port/db` (см. `DbConfig.sqlalchemy_db_uri`).

## Запуск
- Локально: `uvicorn app.main:app` (через `app/main.py`).
- Docker/docker-compose: описан в `README.md`.

## Миграции
- Alembic: `env.py` подставляет `DB_URL`, `target_metadata = app.models.Base.metadata`.
