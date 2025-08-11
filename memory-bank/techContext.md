# Tech Context

## Технологии
- Backend: FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL, Prometheus, Elastic/Kibana, Grafana, Loki/Promtail.
- Mobile: Flutter 3.32.x, Dart 3.8.x, Riverpod, GoRouter, Dio, Freezed, json_serializable, flutter_secure_storage.

## ENV (из README и `app/core/settings.py`)
- USE_COLOR=true
- APP_HOST=0.0.0.0
- APP_PORT=8000
- WORKERS=1
- RELOAD=true
- DB__USER, DB__PASSWORD, DB__NAME
- DB__HOST=postgres (или localhost)
- DB__PORT=5432 (локально 15432→5432)
- DB__ECHO=true
- DOCKER_NAME=rental_app
- ENVIRONMENT=local
- SENTRY_DSN (опционально)

## Порты (docker-compose)
- Backend: 8000
- PostgreSQL: 15432→5432
- Grafana: 3000
- Prometheus: 9090
- Loki: 3100
- Promtail: 9080
- postgres_exporter: 9187
- Elasticsearch: 9200
- Kibana: 5601

## Docker/Docker-compose команды
- Запуск: `docker-compose up --build`
- Локально (без Docker): `uv sync && uvicorn app.main:app --reload`
- Миграции: `alembic upgrade head`
- K8s build/push: `bash k8s/build_push.sh`
- K8s apply: `make kube_run`, удалить: `make kube_del`

## API базовый URL
- Локально: `http://localhost:8000`
- Префикс API: `/v1` → базовый URL для клиента: `http://localhost:8000/v1`

## Web-прогон (Playwright)
- Сборка: `cd mobile_app && flutter build web --release`
- Сервер: `python3 -m http.server 9000 -d build/web`
- Скрипты: `npm run pw:check` (главная), `npm run pw:all` (все ключевые маршруты)

