# 🚀 Быстрый старт FastStream Subscriber

## Что создано

✅ **Dockerfile** - образ для запуска FastStream сервисов
✅ **docker-compose.yml** - оркестрация контейнеров
✅ **Makefile** - команды для управления
✅ **run.sh** - bash скрипт для быстрого запуска
✅ **Интеграция** с основным проектом

## 🏃‍♂️ Быстрый запуск

### Вариант 1: Интеграция с основным проектом

```bash
# Запуск всей инфраструктуры
docker-compose up -d

# Запуск только FastStream
docker-compose up -d fs-broker fs-docs
```

### Вариант 2: Независимый запуск

```bash
cd fs_subscriber

# Создать .env из примера
cp env.example .env

# Запустить все сервисы
./run.sh

# Или по отдельности
./run.sh broker    # Только брокер
./run.sh docs      # Только Swagger
```

## 🎯 Доступные сервисы

| Сервис | Порт | Описание |
|--------|------|----------|
| **fs-broker** | - | FastStream брокер для обработки сообщений |
| **fs-docs** | 8081 | Swagger документация |
| **kafka** | 9092/29092 | Kafka брокер |

## 📋 Основные команды

```bash
# В корне проекта
make fs-broker      # Запустить брокер
make fs-docs        # Запустить документацию
make fs-logs        # Показать логи
make fs-status      # Статус сервисов

# В папке fs_subscriber
./run.sh broker     # Запустить брокер
./run.sh docs       # Запустить документацию
./run.sh logs       # Показать логи
./run.sh status     # Статус контейнеров
```

## 🔧 Конфигурация

Основные настройки в `.env`:

```bash
FS__FASTSTREAM__KAFKA_URL=kafka:9092
FS__FASTSTREAM__SUBJECT=user-register
FS__LOGGING__LOG_LEVEL=info
```

## 🌐 Доступ к сервисам

- **Swagger UI**: http://localhost:8081
- **Kafka (локально)**: localhost:29092
- **Kafka (Docker)**: kafka:9092

## 🐛 Troubleshooting

### Проблемы с подключением к Kafka
```bash
# Проверить статус Kafka
docker-compose ps kafka

# Перезапустить Kafka
docker-compose restart kafka
```

### Проблемы с портами
```bash
# Проверить занятые порты
lsof -i :8081

# Остановить конфликтующий сервис
docker-compose stop fs-docs
```

### Пересборка образов
```bash
docker-compose build fs-broker fs-docs
```

## 📚 Дополнительная документация

- [README.md](README.md) - Подробное описание
- [INTEGRATION.md](INTEGRATION.md) - Интеграция с основным проектом
- [Makefile](Makefile) - Все доступные команды

## 🎉 Готово!

После запуска у вас будет:
- ✅ FastStream брокер для обработки сообщений
- ✅ Swagger документация на порту 8081
- ✅ Интеграция с Kafka
- ✅ Hot reload для разработки
- ✅ Мониторинг и логирование
