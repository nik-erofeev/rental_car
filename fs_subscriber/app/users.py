from faststream import Logger
from faststream.kafka import KafkaRouter

from fs_subscriber.app.settings import APP_CONFIG
from fs_subscriber.app.shemas import UserSendKafka

roter = KafkaRouter()


@roter.subscriber(APP_CONFIG.faststream.subject)
async def send_example_email(
    user: UserSendKafka,
    logger: Logger,
) -> None:
    # todo: документация подтягивается в сваггер docs async api
    """
    Обработка регистрации пользователя:
      — отправка пользователю приветственного письма;
      — ведение журнала.
    """

    logger.info(
        "Sending example email to %s",
        user.email,
    )

    ...
