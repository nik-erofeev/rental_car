# Активный контекст

## Сделано
- Исправлена/расширена модель `User`: email (уникальный), is_active, full_name, phone, role(enum), updated_at; добавлены связи `orders`, `reviews`.
- Обновлены схемы/сервисы пользователей под минимальный CRUD.
- Добавлена модель `Car` со всеми полями по ТЗ и явным `__tablename__`; добавлены связи `photos`, `reports`, `reviews`, `orders`.
- Добавлены модели: `car_photos`, `orders`, `deliveries`, `payments`, `car_reports`, `reviews` + связи между ними.
- Все модели импортированы в `app/models/__init__.py` для Alembic.
- Миграции созданы и применены (по сообщению заказчика).
- Создана и применена ревизия Alembic `7b90ed285194`: добавлены `users.full_name`, `users.phone`, `users.role` (PG ENUM `user_role`), `users.updated_at`; политика — `create_type=False`, управление типами руками через `op.execute("CREATE/DROP TYPE ...").
 - Реализован CRUD для `cars`: добавлены схемы (`use_enum_values=True`), DAO, сервисы и роуты; роутер подключён в приложение.
 - Реализован CRUD для `orders`: добавлены схемы (`use_enum_values=True`, валидация `customer_phone` +7XXXXXXXXXX; в `update` допускается `None`), DAO, сервисы и роуты; роутер подключён.
 - Внедрена централизованная обработка ошибок через `app/api/exceptions.py` для `cars` и `orders`.
 - В `OrderCreate` и `OrderUpdate` ограничены идентификаторы: `car_id > 0`, `user_id` либо `None`, либо `> 0`. Перед созданием заказа проверяется существование `car_id`.
 - `delivery_date` больше не принимается из body при создании/обновлении заказов; значение задаётся на стороне сервера.
 - Реализованы CRUD для `payments` и `deliveries`: добавлены схемы, DAO, сервисы и роуты; роутеры подключены в приложение.
 - Исключения для `payments` и `deliveries` вынесены в `app/api/payments/exceptions.py` и `app/api/deliveries/exceptions.py`.

## Фокус сейчас
 - Добавить CRUD для `reviews` (схемы, DAO, сервисы, роуты), базовые фильтры и сортировку.

## Далее
- CRUD для `car_photos` и `car_reports` (минимальные ручки; каскад на удаление авто уже есть).
- Расширение фильтров/сортировки/пагинации для `cars` и `orders`.
- Интеграционные тесты для основных ручек, фикстуры данных.
- Авторизация/безопасность (при необходимости).
- Мониторинг/логирование: уточнение метрик и форматирования логов.
