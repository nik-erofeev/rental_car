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
 - Рекомендуется вызывать Alembic через бинарь виртуального окружения (без `activate`), используя абсолютные пути:
   ```bash
   /Users/Nik/Desktop/my_test_project/rental_car/.venv/bin/alembic revision --autogenerate -m "Описание изменений"
   /Users/Nik/Desktop/my_test_project/rental_car/.venv/bin/alembic upgrade head
   ```

## Линтеры и pre-commit
- При правках линтов запускать pre-commit для всего репозитория:
  ```bash
  source .venv/bin/activate && pre-commit run --all-files
  ```
  Это гарантирует единый стиль кода и автоматические фиксы (форматирование, импорты и т.п.).
