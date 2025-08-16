import logging

from faststream.kafka import KafkaRouter

from fs_subscriber.settings import APP_CONFIG
from fs_subscriber.shemas import UserSendKafka

roter = KafkaRouter()


logger = logging.getLogger(__name__)


@roter.subscriber(APP_CONFIG.faststream.subject)
async def send_example_email(user: UserSendKafka) -> None:
    # todo: документация подтягивается в сваггер docs async api
    """
    Обработка регистрации пользователя:
      — отправка пользователю приветственного письма;
      — ведение журнала.
    """

    logging.info(
        "Sending example email to %s",
        user.email,
    )

    ...
