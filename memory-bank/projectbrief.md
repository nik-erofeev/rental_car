# Rental Car — Project Brief

## Цели
- Бэкенд FastAPI для аренды авто: CRUD по ключевым сущностям, агрегированные ручки `/{id}/details`, метрики `/metrics`.
- Мобильный фронтенд Flutter: список авто с фильтрами, детали авто, создание заказа, профиль пользователя, отзывы, базовые платежи/доставка.

## Обязательные фичи (MVP)
- Каталог авто (фильтры: make/model/status/engine_type/price/year/sort).
- Детали авто: фото, отчёты, отзывы, связанные заказы.
- Регистрация пользователя (email), профиль пользователя (агрегировано).
- Создание заказа, список заказов, детали заказа (платежи, доставки, авто, пользователь).
- Отзывы: CRUD и привязка к авто/пользователю.
- Платежи/доставки: базовые CRUD и детали.
- Health: `/ping`, `/check_database`. OpenAPI: `/api/v1/openapi.json`.

## Нефункциональные
- Postgres, SQLAlchemy 2.0 (async), Alembic, Prometheus `/metrics`.
- Логи в Elastic (через Filebeat), Kibana/Grafana дашборды.
- CORS, sentry (по `SENTRY_DSN`).

## Deliverables
- Инициализированный memory-bank с живым состоянием.
- Flutter‑приложение с Riverpod, Dio, GoRouter, Freezed и моделями.


