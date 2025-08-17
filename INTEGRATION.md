# Интеграция FastStream Subscriber с основным проектом

## Обзор

FastStream Subscriber интегрирован в основной проект `rental_car` и может запускаться как часть общей инфраструктуры или независимо.

## Способы запуска

### 1. Интеграция с основным проектом

FastStream сервисы добавлены в основной `docker-compose.yml`:

```bash
# Запуск всей инфраструктуры (включая FastStream)
docker-compose up -d

# Запуск только FastStream сервисов
docker-compose up -d fs-broker fs-docs

# Проверка статуса
docker-compose ps fs-broker fs-docs
```

### 2. Независимый запуск

Для разработки и тестирования можно запускать FastStream отдельно:

```bash
cd fs_subscriber

# Запуск всех сервисов
./run.sh

# Запуск только брокера
./run.sh broker

# Запуск только документации
./run.sh docs
```

## Команды Makefile

В корне проекта добавлены команды для управления FastStream:

```bash
# Запуск отдельных сервисов
make fs-broker    # Запустить брокер
make fs-docs      # Запустить Swagger документацию

# Управление
make fs-logs      # Показать логи
make fs-status    # Показать статус
make fs-restart   # Перезапустить сервисы
```

## Конфигурация

### Переменные окружения

Основные настройки в `.env` файле:

```bash
# FastStream конфигурация
FS__FASTSTREAM__KAFKA_URL=kafka:9092
FS__FASTSTREAM__SUBJECT=user-register

# Логирование
FS__LOGGING__LOG_LEVEL=info
```

### Интеграция с Kafka

FastStream использует ту же Kafka инстанс, что и основной проект:

- **Внутри Docker**: `kafka:9092`
- **С хоста**: `localhost:29092`

## Архитектура интеграции

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Main API      │    │  FastStream     │    │     Kafka      │
│   (Port 8000)   │    │   Subscriber    │    │   (Port 9092)  │
│                 │    │                 │    │                 │
│ - Users         │    │ - Broker        │    │ - Topics       │
│ - Cars          │    │ - Swagger Docs  │    │ - Messages     │
│ - Orders        │    │ (Port 8081)     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      Docker Network       │
                    │        (custom)           │
                    └───────────────────────────┘
```

## Мониторинг и логи

### Логи

```bash
# Логи всех FastStream сервисов
make fs-logs

# Логи конкретного сервиса
docker-compose logs -f fs-broker
docker-compose logs -f fs-docs
```


## Разработка

### Hot Reload

Для разработки с автоматической перезагрузкой:

```bash
# В отдельном терминале
make fs-broker

# Изменения в коде автоматически перезагружают сервис
```

### Отладка

```bash
# Подключение к контейнеру
docker-compose exec fs-broker bash
docker-compose exec fs-docs bash

# Просмотр логов в реальном времени
docker-compose logs -f fs-broker
```

## Troubleshooting

### Проблемы с подключением

1. **Kafka недоступна**:
   ```bash
   # Проверить статус Kafka
   docker-compose ps kafka
   
   # Перезапустить Kafka
   docker-compose restart kafka
   ```

2. **Порт 8081 занят**:
   ```bash
   # Проверить, что использует порт
   lsof -i :8081
   
   # Остановить конфликтующий сервис
   docker-compose stop fs-docs
   ```

### Проблемы с зависимостями

1. **Пересобрать образы**:
   ```bash
   docker-compose build fs-broker fs-docs
   ```

2. **Очистить кэш**:
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up -d
   ```

## Производительность

### Оптимизация

- **Memory**: FastStream контейнеры используют минимальные ресурсы
- **CPU**: Асинхронная обработка сообщений
- **Network**: Оптимизированное взаимодействие с Kafka

### Масштабирование

```bash
# Горизонтальное масштабирование брокера
docker-compose up -d --scale fs-broker=3

# Проверка статуса
docker-compose ps fs-broker
```

## Безопасность

- **Network isolation**: FastStream сервисы в отдельной Docker сети
- **Environment variables**: Конфиденциальные данные через `.env`
- **Health checks**: Автоматическая проверка работоспособности

## Деплой

### Production

```bash
# Сборка production образов
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Запуск production окружения
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Development

```bash
# Запуск development окружения
docker-compose up -d

# С hot reload для разработки
make fs-broker
```
