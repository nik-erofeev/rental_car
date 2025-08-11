# Active Context

## Текущий фокус
- Инициализация мобильного проекта и сетевого слоя, подготовка memory-bank, составление карты эндпоинтов/моделей.

## Сделано
- Собраны ENV/порты/команды из `README.md` и `docker-compose.yml`.
- Извлечены роуты и схемы из `app/api/**/routers.py` и `schemas.py`.
- Установлен Flutter 3.32.8; создан проект `mobile_app` (iOS/Android/Web/macOS).
- Добавлены зависимости: Dio, Riverpod (+generator), GoRouter, Freezed, json_serializable, secure storage; сгенерированы модели для `Car` и `CarDetails`.
- Реализован `ApiClient` с интерцептором Bearer и secure storage.
- Добавлен интерцептор завершающего слэша для всех запросов (`_TrailingSlashInterceptor`).
- Настроен базовый URL `http://localhost:8000/v1`.
- Экспортирован OpenAPI в `mobile_app/lib/swagger/swagger.json` и подключена генерация моделей (`swagger_dart_code_generator`) → файлы в `lib/generated/*`.
- Реализован `CarsRepository` и экран `CarsListScreen` с использованием `AsyncValue`.
 - Добавлены: `OrdersRepository`, `UsersRepository`, экраны `OrdersListScreen`, `UserProfileScreen`; настроен GoRouter.
- Добавлен экран `CarDetailsScreen` и маршрут `/cars/:id`.
- Web: используется hash-навигация (`#/orders`, `#/users/1`, `#/cars/1`) для статической выдачи без 404.
- Playwright-скрипты: `tooling/playwright_check.mjs` и `tooling/playwright_all.mjs`; npm-скрипты `pw:check`, `pw:all`.
- Стабильный прогон Playwright (скриншоты в `mobile_app/tooling/*`).

## Дальше
- Использовать сгенерированные модели для сущностей: `User`, `Order`, `OrderDetails`, `Payment`, `Delivery`, `Review`, `CarPhoto`, `CarReport` (доступны в `lib/generated/*`).
- Репозитории и провайдеры для: orders, users, reviews, payments, deliveries; экраны: детали авто/заказа/профиль/создание заказа.
- Проверка macOS: выданы entitlements на сетевые соединения; запуск успешный, список авто загружается.
- Добавить экраны `Payments`, `Deliveries`, `Reviews`; интеграцию форм создания заказа/отзыва.
- Подключить обработку ошибок через `AsyncValue` и вывод в `SelectableText.rich`.
- (Опционально) Автогенерация из OpenAPI (`/api/v1/openapi.json`).

## Решения
- State management: Riverpod.
- Навигация: GoRouter.
- Хранение токена: `flutter_secure_storage`.
