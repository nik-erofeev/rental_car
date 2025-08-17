.PHONY: help build up down logs clean broker docs kafka-only

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Собрать образы
	docker-compose build

up: ## Запустить все сервисы
	docker-compose up -d

down: ## Остановить все сервисы
	docker-compose down

logs: ## Показать логи всех сервисов
	docker-compose logs -f

broker-logs: ## Показать логи брокера
	docker-compose logs -f fs-broker

docs-logs: ## Показать логи Swagger документации
	docker-compose logs -f fs-docs

kafka-logs: ## Показать логи Kafka
	docker-compose logs -f kafka

broker: ## Запустить только брокер
	docker-compose up -d fs-broker

docs: ## Запустить только Swagger документацию
	docker-compose up -d fs-docs

kafka-only: ## Запустить только Kafka и Zookeeper
	docker-compose up -d kafka zookeeper

clean: ## Остановить и удалить все контейнеры, образы и volumes
	docker-compose down -v --rmi all

restart: down up ## Перезапустить все сервисы

status: ## Показать статус контейнеров
	docker-compose ps
