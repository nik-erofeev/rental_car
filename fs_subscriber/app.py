import logging

from faststream import FastStream

from fs_subscriber.brokers import broker
from fs_subscriber.settings import APP_CONFIG
from fs_subscriber.users import roter as users_roter

app = FastStream(
    broker=broker,
)

# faststream run app.fs_subscriber.app:app
# todo: подключаем события subscriber (консюмера)
broker.include_router(users_roter)

# example for docs - дял демо (подключили еще publisher в доку)
publisher = broker.publisher(APP_CONFIG.faststream.subject)


# по дефолту уровень логирования WARNING, поэтому меняем
@app.after_startup
async def configure_logging() -> None:
    logging.basicConfig(
        level=APP_CONFIG.logging.log_level_value,
        format=APP_CONFIG.logging.log_format,
        datefmt=APP_CONFIG.logging.date_format,
    )


# todo: запуск брокера на чтение
# faststream run fs_subscriber.app:app --reload

# запуск сваггера на DOCS async api
# faststream docs serve fs_subscriber.app:app --port 8081

# if __name__ == "__main__":
#     import asyncio
#
#     asyncio.run(app.run())
