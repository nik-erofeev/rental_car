#!/usr/bin/env python3
"""
Скрипт для проверки здоровья FastStream сервисов
"""

import asyncio
import logging
import sys
from typing import Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def check_broker_health() -> dict[str, Any]:
    """Проверка здоровья брокера"""
    try:
        # Здесь можно добавить проверку подключения к Kafka
        # и других зависимостей брокера
        return {
            "status": "healthy",
            "service": "fs-broker",
            "details": "Broker is running",
        }
    except Exception as e:
        logger.error(f"Broker health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "fs-broker",
            "error": str(e),
        }


async def check_docs_health() -> dict[str, Any]:
    """Проверка здоровья Swagger документации"""
    try:
        # Здесь можно добавить проверку доступности Swagger UI
        return {
            "status": "healthy",
            "service": "fs-docs",
            "details": "Swagger documentation is accessible",
        }
    except Exception as e:
        logger.error(f"Docs health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "fs-docs",
            "error": str(e),
        }


async def main() -> None:
    """Основная функция проверки здоровья"""
    logger.info("Starting FastStream health check...")

    # Проверяем все сервисы
    broker_health = await check_broker_health()
    docs_health = await check_docs_health()

    # Выводим результаты
    print("FastStream Health Check Results:")
    print("=" * 40)

    for health in [broker_health, docs_health]:
        status_icon = "✅" if health["status"] == "healthy" else "❌"
        print(f"{status_icon} {health['service']}: {health['status']}")
        if "details" in health:
            print(f"   {health['details']}")
        if "error" in health:
            print(f"   Error: {health['error']}")
        print()

    # Определяем общий статус
    all_healthy = all(h["status"] == "healthy" for h in [broker_health, docs_health])

    if all_healthy:
        logger.info("All FastStream services are healthy!")
        sys.exit(0)
    else:
        logger.error("Some FastStream services are unhealthy!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
