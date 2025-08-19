from faststream.asgi import AsgiFastStream, make_ping_asgi
from faststream.kafka import KafkaBroker
from faststream.kafka.prometheus import KafkaPrometheusMiddleware
from prometheus_client import REGISTRY, make_asgi_app

from fs_subscriber.app.settings import APP_CONFIG
from fs_subscriber.app.users import roter as users_roter

# broker = KafkaBroker(
#     APP_CONFIG.faststream.kafka_url,
# )


# app = FastStream(
#     broker=broker,
# )


# from prometheus_client import CollectorRegistry
# REGISTRY = CollectorRegistry()

# Метрики: используем глобальный REGISTRY, чтобы Prometheus видел стандартные метрики
prometheus_middleware = KafkaPrometheusMiddleware(registry=REGISTRY)

broker = KafkaBroker(
    bootstrap_servers=APP_CONFIG.faststream.kafka_url,
    middlewares=[prometheus_middleware],
)

app = AsgiFastStream(
    broker,
    asgi_routes=[
        ("/health", make_ping_asgi(broker)),
        ("/metrics", make_asgi_app()),
    ],
)


# faststream run app.fs_subscriber.app:app
# todo: подключаем события subscriber (консюмера)
broker.include_router(users_roter)

# example for docs - дял демо (подключили еще publisher в доку)
publisher = broker.publisher(APP_CONFIG.faststream.subject)


# по дефолту уровень логирования WARNING, поэтому меняем (не прокидывать "logger: Logger" в параметрах)
# @app.after_startup
# async def configure_logging() -> None:
#     logging.basicConfig(
#         level=APP_CONFIG.logging.log_level_value,
#         format=APP_CONFIG.logging.log_format,
#         datefmt=APP_CONFIG.logging.date_format,
#     )


# todo: запуск брокера на чтение
# faststream run fs_subscriber.app:app --reload

# запуск сваггера на DOCS async api
# faststream docs serve fs_subscriber.app:app --port 8081

# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(app.run())
