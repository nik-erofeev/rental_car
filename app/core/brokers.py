__all__ = (
    "broker",
    "user_registerer",
)

import logging

from faststream.kafka import KafkaBroker

from app.core.settings import APP_CONFIG

logger = logging.getLogger(__name__)


broker = KafkaBroker(
    APP_CONFIG.faststream.kafka_url,
)

# example for docs - дял демо (подключили еще publisher в доку)
user_registerer = broker.publisher(APP_CONFIG.faststream.subject)
