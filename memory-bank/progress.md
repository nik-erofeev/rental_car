# Progress

## Что работает
- Бэкенд API: CRUD и `details` по users/cars/orders/payments/deliveries/reviews/car_photos/car_reports.
- Health: `/ping`, `/check_database`; OpenAPI `/api/v1/openapi.json`; метрики `/metrics`.
- Мобильный проект создан; сеть и базовые модели готовы.
- Экраны: каталог авто, детали авто, список заказов, профиль пользователя.
- Playwright-проверки Web: главная + ключевые маршруты.

## Что осталось
- Остальные Dart‑модели и маппинг JSON.
- Репозитории/провайдеры и экраны MVP.
- Настройка Android SDK/CocoaPods (Flutter doctor: Android toolchain/CocoaPods).

## Известные проблемы
- Нет явной авторизации (логин/refresh) в бэкенде; используется публичная регистрация email.
- Realtime отсутствует (нет ws/sse/notifications).

## Статус
- Инициализация завершена, можно переходить к реализации экранов и репозиториев.

