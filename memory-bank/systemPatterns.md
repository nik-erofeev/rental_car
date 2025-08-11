# System Patterns

## Бэкенд (FastAPI)
- Слои: API (routers) → Services → DAO → Models.
- Асинхронный SQLAlchemy, `selectinload` для связей.
- Роутеры подключаются в `app/application.py::_init_routes`.
- Метрики: `prometheus_fastapi_instrumentator` + кастом в `app/metrics.py`.
- OpenAPI: `/api/v1/openapi.json`, префикс API: `/v1`.

## Фронтенд (Flutter)
- State management: Riverpod (`flutter_riverpod`, `hooks_riverpod`).
- Маршрутизация: GoRouter.
- Сеть: Dio + интерцептор авторизации (Bearer) + `flutter_secure_storage`.
- Сеть: глобальный интерцептор добавляет завершающий слэш к путям (`/cars` → `/cars/`),
  чтобы соответствовать требованиям бэкенда.
- Модели: Freezed + `json_serializable`.
- Паттерны: декларативные виджеты, `AsyncValue` для загрузки/ошибок.

### Web
- Hash-навигация по умолчанию: пути вида `#/orders`, `#/users/1`.
- Для чистых URL можно включить `setPathUrlStrategy()` и настроить сервер на отдачу `index.html`.

## Конвенции
- Dart модели используют `snake_case` → поля маппятся вручную через Freezed/JsonKey при необходимости.
- Экраны небольшие, разбивка на компоненты, `const` где возможно, списки через `ListView.builder`.

## Платформенные настройки (macOS)
- Entitlements: `com.apple.security.network.client=true` (исходящие соединения),
  `com.apple.security.network.server=true` (по необходимости),
  опционально `com.apple.security.files.user-selected.read-write=true` для отладки.
