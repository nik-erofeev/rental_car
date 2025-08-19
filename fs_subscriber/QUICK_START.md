# 🚀 Быстрый старт FastStream Subscriber

## Запуск
```bash
cd fs_subscriber
cp env.example .env
./run.sh           # все сервисы
# или
./run.sh broker    # брокер
./run.sh docs      # Swagger
```

## Команды (из корня проекта)
```bash
make fs-broker
make fs-docs
make fs-logs
make fs-status
```

## Порты
- Swagger: http://localhost:8081
- Kafka: 9092 (Docker) / 29092 (host)

## Конфигурация (.env)
```bash
FS__FASTSTREAM__KAFKA_URL=kafka:9092
FS__FASTSTREAM__SUBJECT=user-register
FS__LOGGING__LOG_LEVEL=info
```

## Troubleshooting
- Kafka: `docker-compose ps kafka` → `docker-compose restart kafka`
- Порт 8081: `lsof -i :8081` → `docker-compose stop fs-docs`
- Пересборка: `docker-compose build fs-broker fs-docs`

## Docs
- README.md, INTEGRATION.md, Makefile

