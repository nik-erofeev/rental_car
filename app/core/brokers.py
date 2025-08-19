__all__ = (
    "broker",
    "user_registerer",
)

import logging

from faststream.kafka import KafkaBroker
from faststream.kafka.prometheus import KafkaPrometheusMiddleware
from prometheus_client import REGISTRY

from app.core.settings import APP_CONFIG

logger = logging.getLogger(__name__)

# CollectorRegistry(): вы создаёте НОВЫЙ пустой реестр.
# from prometheus_client import CollectorRegistry
# REGISTRY = CollectorRegistry()

# Прометей-метрики для публикаций из backend
# REGISTRY: глобальный реестр по умолчанию (singleton) из prometheus_client.
prometheus_middleware = KafkaPrometheusMiddleware(registry=REGISTRY)

broker = KafkaBroker(
    APP_CONFIG.faststream.kafka_url,
    middlewares=[prometheus_middleware],
)

# example for docs - дял демо (подключили еще publisher в доку)
user_registerer = broker.publisher(APP_CONFIG.faststream.subject)
