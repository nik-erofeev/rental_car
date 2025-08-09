# Системные паттерны и решения

## Архитектура
- FastAPI: пул движка и async_sessionmaker хранятся в app.state (см. `app/application.py`).
- Зависимости сессии: `get_session_without_commit` / `get_session_with_commit` в `app/db.py`.
- Слои: `api` (роуты, схемы, сервисы) → `dao` (работа с БД) → `models`.

## SQLAlchemy
- Базовый класс `app.db.Base` предоставляет `id`, `created_at` и авто-`__tablename__`.
- Правило проекта: явно задаём `__tablename__` в каждой модели.
- Для Alembic все модели импортируются в `app/models/__init__.py` (autogenerate видит изменения).

### ENUM в PostgreSQL
- В моделях использовать ENUM с явным именем типа и отключённым автосозданием типа:
  - Вариант с диалектом PG:
    ```python
    from sqlalchemy.dialects.postgresql import ENUM as PGEnum
    role: Mapped[UserRole] = mapped_column(PGEnum('customer', 'manager', 'admin', name='user_role', create_type=False))
    ```
  - Либо через `sqlalchemy.Enum(..., name='user_role')` при условии, что тип уже существует в БД и автосоздание отключено.
- В миграциях при добавлении/удалении колонок с ENUM тип не создаём автоматически (политика: `create_type=False`).
  - Типы создаются отдельно (в первичных миграциях) или руками при необходимости через `op.execute("CREATE TYPE ... AS ENUM (...)")`.
  - В `downgrade()` при удалении последних использований типа — руками удаляем тип:
    ```python
    # todo: для ENUM руками — alembic не удаляет
    op.execute("DROP TYPE IF EXISTS user_role CASCADE;")
    ```
- Если ENUM используется в нескольких таблицах, тип удаляем только тогда, когда он больше нигде не используется (как правило, в последней ревизии цепочки изменений).

## Pydantic v2
- Схемы чтения используют `model_config = {from_attributes=True}` для валидации ORM-объектов.
- Для перечислений используем `use_enum_values=True`, чтобы в API возвращались строковые значения enum.
- Валидация телефонов для заказов: `+7XXXXXXXXXX` через `@field_validator('customer_phone')`.
  - В `OrderCreate` — поле обязательно и валидируется.
  - В `OrderUpdate` — поле опционально; валидатор пропускает `None`.
- Поле `delivery_date` в заказах не передаётся в body (create/update); значение формируется и обновляется на стороне сервера по бизнес‑правилам.

## Исключения и обработка ошибок
- Централизованные исключения определены в `app/api/exceptions.py` и используются в сервисах.
  - Cars: `CarNotFoundException` (404), `CarAlreadyExistsException` (409).
  - Orders: `OrderNotFoundException` (404), `OrderCarNotFoundException` (404).
- В сервисах не бросаем `ValueError`; вместо этого поднимаем готовые `HTTPException` из `app.api.exceptions`.
- Перед созданием зависимых сущностей проверяем наличие FK-объектов (например, `car_id` для `orders`). При отсутствии — 404.
- Для полей с идентификаторами в схемах указывать ограничения: `gt=0` для `car_id`, `user_id` (если не `None`).

## Наблюдаемость
- `prometheus-fastapi-instrumentator` подключён.

## Стиль
- Предпочтительная длина строки: 120.

## Контроль качества кода
- При исправлении замечаний линтера запускать hooks через pre-commit для всех файлов:
  ```bash
  source .venv/bin/activate && pre-commit run --all-files
  ```
