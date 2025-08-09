# Активный контекст

## Сделано
- Исправлена/расширена модель `User`: email (уникальный), is_active, full_name, phone, role(enum), updated_at; добавлены связи `orders`, `reviews`.
- Обновлены схемы/сервисы пользователей под минимальный CRUD.
- Добавлена модель `Car` со всеми полями по ТЗ и явным `__tablename__`; добавлены связи `photos`, `reports`, `reviews`, `orders`.
- Добавлены модели: `car_photos`, `orders`, `deliveries`, `payments`, `car_reports`, `reviews` + связи между ними.
- Все модели импортированы в `app/models/__init__.py` для Alembic.
- Миграции созданы и применены (по сообщению заказчика).
- Создана и применена ревизия Alembic `7b90ed285194`: добавлены `users.full_name`, `users.phone`, `users.role` (PG ENUM `user_role`), `users.updated_at`; политика — `create_type=False`, управление типами руками через `op.execute("CREATE/DROP TYPE ...").

## Фокус сейчас
- Реализовать CRUD для `cars`: схемы, DAO, сервисы, роуты, подключение в приложение.

## Далее
- Расширение доменной модели (photos, orders, payments и т.д.).
- Авторизация/безопасность (при необходимости).
