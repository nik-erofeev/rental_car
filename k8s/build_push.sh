#!/usr/bin/env bash
set -euo pipefail

# Скрипт: собрать локальный образ из Dockerfile в корне и запушить в Docker Hub как nikerofeev/rental_car:latest

IMAGE_NAME="nikerofeev/rental_car"
IMAGE_TAG="latest"

echo "[build_push] Сборка образа ${IMAGE_NAME}:${IMAGE_TAG} из корня репозитория..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "[build_push] Пуш образа в Docker Hub..."
docker push ${IMAGE_NAME}:${IMAGE_TAG}

echo "[build_push] Готово: ${IMAGE_NAME}:${IMAGE_TAG}"


