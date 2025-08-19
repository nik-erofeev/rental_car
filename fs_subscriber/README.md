# FastStream Subscriber

Минимальный набор для запуска FastStream брокера и Swagger‑документации.

## Быстрый старт
```bash
cp env.example .env
make up
make status
```

## Команды
- build/up/down/restart
- logs | broker-logs | docs-logs | kafka-logs
- broker | docs | kafka-only
- status | clean | help

## Доступ
- Swagger: http://localhost:8081
- Kafka (локально): localhost:29092
- Kafka (Docker): kafka:9092

## Конфигурация (.env)
```bash
FS__FASTSTREAM__KAFKA_URL=kafka:9092
FS__FASTSTREAM__SUBJECT=user-register
FS__LOGGING__LOG_LEVEL=info
```

## Разработка
```bash
make broker     # hot-reload брокера
make docs       # документация
```

## Очистка
```bash
make clean
```

## Структура
```
fs_subscriber/
├── app/              # код приложения
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── run.sh
└── env.example
```