from enum import StrEnum, unique

from dotenv import find_dotenv
from pydantic import BaseModel, HttpUrl, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_file=find_dotenv(".env"),
    )


@unique
class Environments(StrEnum):
    local = "local"
    qa = "qa"
    stage = "stage"
    prod = "prod"
    test = "test"


class DbConfig(Config):
    model_config = SettingsConfigDict(env_prefix="DB__")
    user: str  # = ""
    password: str  # = ""
    host: str  # = ""
    port: int  # = 5432
    name: str  # = ""

    max_size: int = 1
    echo: bool = True

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_db_uri(self) -> PostgresDsn:
        multi_host_url = MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )

        return PostgresDsn(str(multi_host_url))


class Api(BaseModel):
    project_name: str = "Rental_Car"
    description: str = "Rental_Car API 🚀"
    version: str = "1.0.0"
    openapi_url: str = "/api/v1/openapi.json"
    echo: bool = False
    v1: str = "/v1"


class FaststreamConfig(Config):
    kafka_url: str  # = "kafka:9092" or "localhost:29092"
    subject: str  # = "user-register"

    model_config = SettingsConfigDict(env_prefix="FS__")


class AppConfig(Config):
    sentry_dsn: HttpUrl | None = None
    use_color: bool = False  # true = цветной вывод в консоль; false = обычная консоль   # noqa: E501
    app_host: str
    app_port: int
    workers: int
    reload: bool

    db: DbConfig = DbConfig()
    api: Api = Api()
    cors_origin_regex: str = r"(http://|https://)?(.*\.)?(qa|stage|localhost|0.0.0.0)" r"(\.ru)?(:\d+)?$"
    # environment: Environments = Environments.local

    # JWT/Безопасность
    # переопределить в .env (openssl rand -hex 32)
    secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    faststream: FaststreamConfig = FaststreamConfig()  # type: ignore


APP_CONFIG = AppConfig()  # type: ignore
