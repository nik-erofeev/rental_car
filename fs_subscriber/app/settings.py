import logging
from typing import Literal

from dotenv import find_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"

WORKER_LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d][%(processName)s] %(module)16s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_file=find_dotenv(".env"),
    )


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class FaststreamConfig(Config):
    kafka_url: str  # = "kafka:9092" or "localhost:29092"
    subject: str  # = "user-register"

    model_config = SettingsConfigDict(env_prefix="FS__")


class Configs(Config):
    faststream: FaststreamConfig = FaststreamConfig()  # type: ignore
    logging: LoggingConfig = LoggingConfig()

    model_config = SettingsConfigDict(env_prefix="FS__")


APP_CONFIG = Configs()
