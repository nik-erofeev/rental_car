# Интеграция FastStream Subscriber

Коротко о запуске FastStream в составе проекта и отдельно.

## Запуск

### В составе проекта
```bash
docker-compose up -d               # вся инфраструктура
docker-compose up -d fs-broker fs-docs
docker-compose ps fs-broker fs-docs
```

### Отдельно
```bash
cd fs_subscriber
./run.sh            # все сервисы
./run.sh broker     # только брокер
./run.sh docs       # только Swagger
```

## Makefile (корень)
```bash
make fs-broker
make fs-docs
make fs-logs
make fs-status
make fs-restart
```

## Конфигурация
`.env` (ключевое):
```bash
FS__FASTSTREAM__KAFKA_URL=kafka:9092
FS__FASTSTREAM__SUBJECT=user-register
FS__LOGGING__LOG_LEVEL=info
```

Kafka:
- В Docker: `kafka:9092`
- С хоста: `localhost:29092`

## Логи и разработка
```bash
make fs-logs
docker-compose logs -f fs-broker
docker-compose logs -f fs-docs

# hot reload
make fs-broker
```

## Troubleshooting
- Kafka не доступна: `docker-compose ps kafka` → `docker-compose restart kafka`
- Порт 8081 занят: `lsof -i :8081` → `docker-compose stop fs-docs`
- Пересборка: `docker-compose build fs-broker fs-docs`
- Чистый запуск: `docker-compose down && docker system prune -f && docker-compose up -d`

## Масштабирование
```bash
docker-compose up -d --scale fs-broker=3
docker-compose ps fs-broker
```

## Доступ
- Swagger: http://localhost:8081
- Kafka (локально): localhost:29092
- Kafka (Docker): kafka:9092
