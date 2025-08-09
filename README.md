## Rental Car API — FastAPI backend

### О проекте
- Бэкенд для сервиса аренды авто: CRUD по ключевым сущностям, расширенные фильтры, агрегированные ручки
  `/{id}/details`.
- Технологии: FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL. Метрики Prometheus на `/metrics`.

### Структура проекта
```
.
  app/
    api/              # роуты, схемы, сервисы по сущностям
    core/             # настройки
    dao/              # слой доступа к данным (DAO)
    models/           # модели SQLAlchemy
    application.py    # сборка FastAPI-приложения
    main.py           # точка входа (uvicorn)
    db.py             # базовые утилиты БД
  migrations/
    env.py            # конфиг Alembic (async)
    script.py.mako    # шаблон ревизии
    versions/         # файлы миграций
  alembic.ini
  example_crud_api.bash
```

### Быстрый старт (локально)
1) Виртуальное окружение и зависимости
```bash
python -m venv .venv
source .venv/bin/activate
pip install uv
uv sync
```

2) Окружение (.env)
- Скопируйте пример и отредактируйте при необходимости:
```bash
cp .env_example .env
```
- Ключевые переменные (пример):
```dotenv
# Приложение
APP_HOST=localhost
APP_PORT=8000
WORKERS=1
RELOAD=true

# База данных
DB__USER=user
DB__PASSWORD=pass
DB__NAME=rental_car
DB__ECHO=true

# Вариант 1: Docker (контейнер postgres)
DB__HOST=postgres
DB__PORT=5432

# Вариант 2: Локальный PostgreSQL (порт из docker-compose)
# DB__HOST=localhost
# DB__PORT=15432

DOCKER_NAME=rental
ENVIRONMENT=local
```

3) Миграции БД
```bash
alembic upgrade head
```

4) Запуск приложения
```bash
uvicorn app.main:app --reload
```
OpenAPI: `http://localhost:8000/docs`.

### Запуск в Docker (опционально)
```bash
docker-compose up --build
```
- Backend: `http://localhost:8000`
- PostgreSQL публикуется на `15432`

### Модель данных (упрощённо, без авторизации)
- **users**: id, email (uniq), full_name, phone, role (customer|manager|admin), is_active,
  created_at, updated_at
- **cars**: id, vin (uniq), make, model, year, mileage, price, condition (new|used), color,
  engine_type (gasoline|diesel|hybrid|electric), transmission (manual|automatic|cvt),
  status (available|reserved|sold), description, created_at, updated_at
- **car_photos**: id, car_id → cars.id, url, is_main
- **orders**: id, car_id → cars.id, customer_name/phone/email, status (pending|paid|processing|
  in_delivery|completed|canceled), payment_method (cash|card|loan|lease), total_amount,
  delivery_address, delivery_date, created_at, updated_at
- **deliveries**: id, order_id → orders.id, status (pending|in_progress|delivered|failed),
  tracking_number, delivered_at
- **payments**: id, order_id → orders.id, amount, status (pending|paid|failed),
  payment_type (full|installment|deposit), transaction_id, paid_at
- **car_reports**: id, car_id → cars.id, report_type (vin_check|technical_inspection), data (JSON),
  created_at
- **reviews**: id, car_id → cars.id, customer_name, rating (1–5), comment, created_at

### Связи (ERD)
- cars ───< car_photos | car_reports | reviews | orders ───< payments
- orders ───< deliveries
- users ───< orders | reviews

### Архитектура (слои)
- API (routers): валидация и описание эндпоинтов, минимум логики
- Services: бизнес-логика, агрегированные ответы, логирование
- DAO: SQLAlchemy-запросы, фильтры/сортировка/пагинация, `selectinload` для связей
- Валидация enum-фильтров в роутерах (422); 404 для пустых результатов — через кастомные исключения

### Миграции Alembic — основные команды
```bash
alembic revision --autogenerate -m "change"
alembic upgrade head
alembic downgrade -1
```

### Примеры запросов
- См. `example_crud_api.bash` — готовые curl-команды для CRUD, фильтров и `details`.
