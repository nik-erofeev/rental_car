# Прогресс

## Работает
- Базовое FastAPI приложение, health-эндпоинты, метрики.
- Пользователи: базовые схемы/сервисы, DAO.
- Модель `Car` и миграции под неё.

## В работе
- CRUD `cars` (роуты/схемы/сервисы/DAO).

## Известные моменты
- Соблюдать правило явного `__tablename__` в моделях.
- Длина строки 120 символов.

## Миграции
- Создана ревизия Alembic: `31a91ebf82a8_add_domain_models_cars_car_photos_.py`
- Описывает таблицы: `car_photos`, `car_reports`, `orders` (с индексами `car_id`, `user_id`), `reviews` (индексы `car_id`, `user_id`), `deliveries` (индекс `order_id`), `payments` (индекс `order_id`).
 - Применена ревизия: `7b90ed285194_описание_изменений.py` — добавлены в `users` поля `full_name`, `phone`, `role` (PG ENUM `user_role`), `updated_at`.
 - Исправлена ошибка PostgreSQL `type "user_role" does not exist` — в ревизию добавлено явное создание/удаление типа ENUM (`CREATE TYPE`/`DROP TYPE`) через `sa.Enum(...).create/drop`.
