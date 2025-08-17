.PHONY: help kube_run kube_del fs-broker fs-docs fs-logs fs-status fs-restart

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Применить все манифесты
kube_run:
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/secret.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/hpa.yaml

# alias
#kaf k8s/configmap.yaml
#kaf k8s/secret.yaml
#kaf k8s/deployment.yaml
#kaf k8s/service.yaml
#kaf k8s/hpa.yaml

# Удалить все манифесты
kube_del:
	kubectl delete -f k8s/configmap.yaml
	kubectl delete -f k8s/secret.yaml
	kubectl delete -f k8s/deployment.yaml
	kubectl delete -f k8s/service.yaml
	kubectl delete -f k8s/hpa.yaml

#alias
#kdelf k8s/configmap.yaml
#kdelf k8s/secret.yaml
#kdelf k8s/deployment.yaml
#kdelf k8s/service.yaml
#kdelf k8s/hpa.yaml

# FastStream Subscriber команды
fs-broker: ## Запустить только FastStream брокер
	docker-compose up -d fs-broker

fs-docs: ## Запустить только FastStream Swagger документацию
	docker-compose up -d fs-docs

fs-logs: ## Показать логи FastStream сервисов
	docker-compose logs -f fs-broker fs-docs

fs-status: ## Показать статус FastStream контейнеров
	docker-compose ps fs-broker fs-docs

fs-restart: ## Перезапустить FastStream сервисы
	docker-compose restart fs-broker fs-docs