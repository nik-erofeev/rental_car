#!/bin/bash

# Entrypoint скрипт для FastStream Subscriber
# Запускает либо брокер, либо Swagger документацию

# Ждем доступности Kafka (по переменной окружения FS__FASTSTREAM__KAFKA_URL)
wait_for_kafka() {
    KAFKA_URL=${FS__FASTSTREAM__KAFKA_URL:-kafka:9092}
    KAFKA_HOST=$(echo "$KAFKA_URL" | cut -d: -f1)
    KAFKA_PORT=$(echo "$KAFKA_URL" | cut -d: -f2)

    echo "⏳ Ожидание Kafka по адресу ${KAFKA_HOST}:${KAFKA_PORT}..."
    for i in $(seq 1 60); do
        if (echo > /dev/tcp/${KAFKA_HOST}/${KAFKA_PORT}) >/dev/null 2>&1; then
            echo "✅ Kafka доступна"
            return 0
        fi
        echo "… нет подключения, попытка ${i}/60"; sleep 1
    done
    echo "❌ Не удалось дождаться Kafka (${KAFKA_HOST}:${KAFKA_PORT})" >&2
    return 1
}

# Проверяем аргумент командной строки
if [ "$1" = "broker" ]; then
    echo "🚀 Запуск FastStream брокера..."
    echo "📡 Брокер будет слушать сообщения Kafka..."
    echo "🔄 Включен hot-reload для разработки..."

    # Ждем Kafka перед стартом
    wait_for_kafka || exit 1

    exec faststream run fs_subscriber.app.main:app --reload --host 0.0.0.0 --port 8000

elif [ "$1" = "docs" ]; then
    echo "📚 Запуск Swagger документации..."
    echo "🌐 Документация будет доступна на порту 8081"
    echo "🔗 Откройте: http://localhost:8081"
    exec faststream docs serve fs_subscriber.app.main:app --port 8081 --host 0.0.0.0

else
    echo "❌ Неизвестная команда: $1"
    echo ""
    echo "📋 Использование: $0 [broker|docs]"
    echo ""
    echo "🔧 Доступные команды:"
    echo "  broker  - Запустить FastStream брокер с hot-reload"
    echo "  docs    - Запустить Swagger документацию на порту 8081"
    echo ""
    echo "💡 Примеры:"
    echo "  $0 broker    # Запустить брокер"
    echo "  $0 docs      # Запустить документацию"
    exit 1
fi
