#!/bin/bash

# Entrypoint скрипт для FastStream Subscriber
# Запускает либо брокер, либо Swagger документацию

# Проверяем аргумент командной строки
if [ "$1" = "broker" ]; then
    echo "🚀 Запуск FastStream брокера..."
    echo "📡 Брокер будет слушать сообщения Kafka..."
    echo "🔄 Включен hot-reload для разработки..."
    exec faststream run fs_subscriber.app:app --reload

elif [ "$1" = "docs" ]; then
    echo "📚 Запуск Swagger документации..."
    echo "🌐 Документация будет доступна на порту 8081"
    echo "🔗 Откройте: http://localhost:8081"
    exec faststream docs serve fs_subscriber.app:app --port 8081 --host 0.0.0.0

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
