### структура

## Backend: структура, миграции Alembic и запуск

### Кратко
- **Стек**: FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL
- **Цель**: простой и масштабируемый бэкенд с асинхронным доступом к БД и управлением схемой через миграции

### Структура каталога `backend`
```
backend/
  app/
    api/              # роуты, схемы, сервисы по сущностям
    core/             # настройки, логирование
    dao/              # слой доступа к данным (DAO)
    models/           # модели SQLAlchemy
    application.py    # сборка FastAPI-приложения
    main.py           # точка входа (uvicorn)
    db.py             # базовые утилиты БД, Base, зависимости сессий
  migrations/
    env.py            # конфигурация Alembic (async), target_metadata
    script.py.mako    # шаблон файла ревизии
    versions/         # файлы миграций
  alembic.ini         # конфиг Alembic (sqlalchemy.url = %(DB_URL)s)
  docker/
    app.sh            # запуск миграций и сервера
  Dockerfile          # образ бэкенда
```

### Конфигурация БД и окружения
- Конфиг приложения — `app/core/settings.py` (`APP_CONFIG`).
  - `DbConfig.sqlalchemy_db_uri` собирается как DSN вида `postgresql+asyncpg://user:pass@host:port/db`.
  - Переменные окружения читаются с разделителем `__` (например, `DB__USER`, `DB__PASSWORD`, `DB__HOST`, `DB__PORT`, `DB__NAME`).
- При старте приложения создаётся async-движок и `session_maker` в `app/application.py`.

### Alembic: как устроено
1) `alembic.ini`
   - Важные опции:
     - `prepend_sys_path = .` — позволяет импортировать модули приложения.
     - `script_location = %(here)s/migrations` — каталог миграций.
     - `sqlalchemy.url = %(DB_URL)s` — URL БД подставляется программно из `env.py`.

2) `migrations/env.py`
   - Подключение конфигурации из приложения и прокидывание `DB_URL`:
     ```python
     from app.core.settings import APP_CONFIG
     section = config.config_ini_section
     config.set_section_option(section, "DB_URL", str(APP_CONFIG.db.sqlalchemy_db_uri))
     ```
   - Цель автогенерации:
     ```python
     from app import models
     target_metadata = models.Base.metadata
     ```
   - Запуск миграций в async-режиме:
     ```python
     connectable = async_engine_from_config(
         config.get_section(config.config_ini_section, {}),
         prefix="sqlalchemy.",
         poolclass=pool.NullPool,
     )
     ```

3) Аггрегация моделей: `app/models/__init__.py`
   - Для того чтобы Alembic видел все таблицы при `--autogenerate`, модели должны быть импортированы в пакет `app.models`:
     ```python
     # app/models/__init__.py
     from .users import *
     ```
   - При добавлении новой модели обязательно добавьте её импорт в этот файл, иначе Alembic не увидит изменения схемы.

4) Шаблон миграции: `migrations/script.py.mako`
   - Шаблон генерирует типизированные поля `revision`, `down_revision` и содержит заготовки `upgrade()`/`downgrade()`.

### Команды Alembic (локально)
- Создать новую ревизию на основе изменений моделей:
  ```bash
  alembic revision --autogenerate -m "Описание изменений"
  ```
- Применить миграции:
  ```bash
  alembic upgrade head
  ```
- Откатить миграции на один шаг:
  ```bash
  alembic downgrade -1
  ```

### Docker / docker-compose
- Приложение запускается через корневой `docker-compose.yml`:
  ```bash
  docker-compose up --build
  ```
  - Backend: `http://localhost:8000`
  - PostgreSQL: порт `15432` на хосте (в контейнере `5432`)

- Миграции в контейнере применяются автоматически в `backend/docker/app.sh`:
  ```sh
  alembic upgrade head
  ```

- Генерация ревизии внутри контейнера (пример):
  ```bash
  docker-compose run --rm backend bash -lc "alembic revision --autogenerate -m 'add new model'"
  ```

### Как добавить новую модель и миграцию
1) Создайте модель в `app/models/<entity>.py` (наследуйте от `app.db.Base`).
2) Импортируйте модель в `app/models/__init__.py`.
3) Сгенерируйте миграцию: `alembic revision --autogenerate -m "..."`.
4) Проверьте содержимое файла в `migrations/versions/` и примените миграции: `alembic upgrade head`.

### Частые проблемы
- Alembic не видит таблицу при `--autogenerate` — проверьте, что модель импортирована в `app/models/__init__.py` и что `target_metadata = models.Base.metadata`.
- Ошибка импорта модулей при запуске Alembic — проверьте `prepend_sys_path = .` в `alembic.ini` и `PYTHONPATH=/app` (в Dockerfile уже указан).
- Нет подключения к БД — проверьте переменные `DB__USER`, `DB__PASSWORD`, `DB__HOST`, `DB__PORT`, `DB__NAME`.

### Переменные окружения (важное)
- Используется разделитель `__` для вложенных настроек Pydantic Settings.
- Минимальный набор:
  - `DB__USER`, `DB__PASSWORD`, `DB__HOST`, `DB__PORT`, `DB__NAME`
  - `SECRET_KEY`, `ALGORITHM`

### Ссылки
- Alembic docs: автогенерация, async-движок, шаблон `script.py.mako`, множественные `MetaData`.

### Упрощённая модель данных (без авторизации)
1. Пользователи (users)
id — PK

email — уникальный

is_active — флаг активности

full_name — полное имя

phone — телефон

role — (customer, manager, admin)

created_at

updated_at

2. Автомобили (cars)
id — PK

vin — уникальный

make — марка (Toyota, BMW...)

model — модель

year — год выпуска

mileage — пробег (км)

price — цена

condition — (new, used)

color

engine_type — (gasoline, diesel, hybrid, electric)

transmission — (manual, automatic, cvt)

status — (available, reserved, sold)

description — текстовое описание

created_at

updated_at

3. Фотографии автомобилей (car_photos)
id — PK

car_id — FK → cars.id

url — путь к изображению

is_main — флаг главного фото

4. Заказы (orders)
id — PK

customer_name — имя клиента

customer_phone — телефон

customer_email — email

car_id — FK → cars.id

status — (pending, paid, processing, in_delivery, completed, canceled)

payment_method — (cash, card, loan, lease)

total_amount — сумма

delivery_address

delivery_date — планируемая доставка

created_at

updated_at

5. Доставка (deliveries)
id — PK

order_id — FK → orders.id

status — (pending, in_progress, delivered, failed)

tracking_number

delivered_at

6. Платежи (payments)
id — PK

order_id — FK → orders.id

amount

status — (pending, paid, failed)

payment_type — (full, installment, deposit)

transaction_id — ID транзакции в платёжной системе

paid_at

7. Отчёты по VIN и диагностике (car_reports)
id — PK

car_id — FK → cars.id

report_type — (vin_check, technical_inspection)

data — JSON (результаты проверки)

created_at

8. Отзывы (reviews)
id — PK

customer_name

car_id — FK → cars.id

rating — 1–5

comment

created_at


### ERD-связи

cars ───< car_photos
cars ───< car_reports
cars ───< reviews
cars ───< orders ───< payments
orders ───< deliveries
users ───< orders
users ───< reviews
