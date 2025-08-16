__all__ = ("broker",)

import logging

from faststream.kafka import KafkaBroker

from fs_subscriber.settings import APP_CONFIG

logger = logging.getLogger(__name__)


broker = KafkaBroker(
    APP_CONFIG.faststream.kafka_url,
)
