#!/bin/bash

# Скрипт для быстрого запуска FastStream сервисов

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    error "Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    error "Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    warn "Файл .env не найден. Создаю из примера..."
    if [ -f "env.example" ]; then
        cp env.example .env
        log "Файл .env создан из env.example"
        warn "Отредактируйте .env файл под ваши нужды перед запуском"
        exit 0
    else
        error "Файл env.example не найден. Создайте .env файл вручную."
        exit 1
    fi
fi

# Функция для показа справки
show_help() {
    echo "Использование: $0 [команда]"
    echo ""
    echo "Команды:"
    echo "  all       - Запустить все сервисы (по умолчанию)"
    echo "  broker    - Запустить только брокер"
    echo "  docs      - Запустить только Swagger документацию"
    echo "  kafka     - Запустить только Kafka и Zookeeper"
    echo "  stop      - Остановить все сервисы"
    echo "  restart   - Перезапустить все сервисы"
    echo "  logs      - Показать логи всех сервисов"
    echo "  status    - Показать статус контейнеров"
    echo "  clean     - Полная очистка"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0          # Запустить все сервисы"
    echo "  $0 broker   # Запустить только брокер"
    echo "  $0 logs     # Показать логи"
}

# Основная логика
case "${1:-all}" in
    "all")
        log "Запуск всех сервисов..."
        docker-compose up -d
        log "Все сервисы запущены!"
        log "Swagger документация доступна по адресу: http://localhost:8081"
        log "Для просмотра логов используйте: $0 logs"
        ;;
    "broker")
        log "Запуск брокера..."
        docker-compose up -d fs-broker
        log "Брокер запущен!"
        ;;
    "docs")
        log "Запуск Swagger документации..."
        docker-compose up -d fs-docs
        log "Swagger документация запущена на порту 8081"
        ;;
    "kafka")
        log "Запуск Kafka и Zookeeper..."
        docker-compose up -d kafka zookeeper
        log "Kafka и Zookeeper запущены!"
        ;;
    "stop")
        log "Остановка всех сервисов..."
        docker-compose down
        log "Все сервисы остановлены!"
        ;;
    "restart")
        log "Перезапуск всех сервисов..."
        docker-compose restart
        log "Все сервисы перезапущены!"
        ;;
    "logs")
        log "Показать логи всех сервисов..."
        docker-compose logs -f
        ;;
    "status")
        log "Статус контейнеров:"
        docker-compose ps
        ;;
    "clean")
        warn "Выполняется полная очистка..."
        docker-compose down -v --rmi all
        log "Очистка завершена!"
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        error "Неизвестная команда: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
