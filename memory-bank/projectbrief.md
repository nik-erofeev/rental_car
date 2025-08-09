# Краткое описание проекта

- Назначение: бэкенд API на FastAPI для управления сущностями автосалона/каталога автомобилей.
- Технологии: FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL, Pydantic v2.
- Архитектура: слои `api/` (роуты, схемы, сервисы), `dao/` (доступ к БД), `models/` (SQLAlchemy), `core/` (настройки), `db.py` (Base, зависимости сессии).
- Миграции: Alembic (autogenerate по `app.models.Base.metadata`, агрегатор моделей — `app/models/__init__.py`).

## Сущности (реализованные модели)
- Users: id, email (уникальный), is_active, full_name, phone, role(enum: customer|manager|admin), created_at, updated_at; связи: `orders`, `reviews`.
- Cars: vin (уникальный), make, model, year, mileage, price, condition, color, engine_type, transmission, status, description, timestamps; связи: `photos`, `reports`, `reviews`, `orders`.
- CarPhotos: `car_id`, `url`, `is_main`.
- Orders: customer_name, customer_phone, customer_email, `user_id?`, `car_id`, status, payment_method, total_amount, delivery_address, delivery_date, timestamps; связи: `deliveries`, `payments`.
- Deliveries: `order_id`, status, tracking_number, delivered_at.
- Payments: `order_id`, amount, status, payment_type, transaction_id, paid_at.
- CarReports: `car_id`, report_type, data.
- Reviews: customer_name, `user_id?`, `car_id`, rating, comment.

## Ключевые правила
- Всегда указывать `__tablename__` в моделях (договорённость проекта).
- Все модели импортировать в `app/models/__init__.py`, чтобы Alembic видел таблицы при `--autogenerate`.
- Лимит длины строки кода — 120 (предпочтение проекта).
- ENUM (PG): в моделях использовать именованные типы и отключать автосоздание (`create_type=False`). Создание/удаление типов выполнять руками в миграциях через `op.execute("CREATE TYPE ...")` и `op.execute("DROP TYPE ... CASCADE")`. Типы удалять только когда они больше нигде не используются.

