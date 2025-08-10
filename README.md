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

# log
USE_COLOR=true

# Приложение
APP_HOST=0.0.0.0
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

DOCKER_NAME=rental_app
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
OpenAPI: http://localhost:8000/docs.

### Запуск в Docker (опционально)
```bash
docker-compose up --build
```
- Backend: `http://localhost:8000`
- PostgreSQL публикуется на `15432`

### Логи и мониторинг (Elasticsearch + Kibana + Grafana dashboard)
- После запуска `docker-compose` поднимутся `elasticsearch`, `kibana` и `filebeat`.
- Kibana: откройте http://localhost:5601.
- Grafana с дашбордами http://localhost:3000
- Data View создаётся автоматически скриптом `docker/elastic/kibana_setup.sh`:
  - **Имя**: `rental_car_api_beckend`
  - **Шаблон индекса**: `filebeat-*`
  - **Поле времени**: `@timestamp`

Шаги для просмотра логов:
1. Зайдите в Kibana → Discover.
2. Выберите Data View `rental_car_api_beckend`.
3. В блоке Selected fields добавьте поля:
   - `container.name`
   - `log.level`
   - `message`
4. Пример запроса поиска (KQL):
   - `container.name: "rental_app_api"`
5. Дополнительные фильтры (KQL):
   - По контейнеру бэкенда:
     - `container.name: "rental_app_api"`
   - По уровню логирования:
     - `log.level: "INFO"` или `log.level: "ERROR"`
   - Поле сообщения:
     - выводится в поле `message`.

Важно:
- Логи будут появляться в Elasticsearch, когда приложение запущено в Docker (Filebeat собирает JSON‑логи контейнера).
- Полезные поля в Discover: `container.name`, `message`, `log.level`.

<br>

## Деплой в Kubernetes (локально/кластер)
1) Собрать и запушить образ (нужен логин в Docker Hub):
```bash
bash k8s/build_push.sh
```
или вручную:
```bash
docker build -t nikerofeev/rental_car:latest .
docker push nikerofeev/rental_car:latest
```

2) Применить манифесты (разнесены по файлам)

    #### должна быть поднята БД в докере
```bash
make kube_run
```

3) Проверить ресурсы:
```bash
kubectl get pods,deploy,svc,hpa
```

4) Пробросить порт сервиса на локальную машину(ЧТОЮЫ РАБОАТЛА API):
```bash
kubectl port-forward service/rental-app-api 8000:80

# можно взять ip и по нему вместо localhost
# читать k8s/service.yaml 18-19 строка!!
# kgp -o wide
```

Примечания:
- В `k8s/deployment.yml` настроены readiness/liveness пробы (`/docs`, `/ping`).
- HPA требует установленный metrics-server.
- Для приватного реестра используйте `imagePullSecrets`.

5) Удаление созданных ресурсов:
```bash
make kube_del
```


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
