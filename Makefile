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