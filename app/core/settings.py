from enum import StrEnum, unique

from dotenv import find_dotenv
from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class Environments(StrEnum):
    local = "local"
    qa = "qa"
    stage = "stage"
    prod = "prod"
    test = "test"


class DbConfig(BaseModel):
    user: str = ""
    password: str = ""
    host: str = ""
    port: int = 5432
    name: str = ""

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


class AppConfig(BaseSettings):
    use_color: bool = False  # true = цветной вывод в консоль; false = обычная консоль   # noqa: E501

    app_host: str
    app_port: int
    workers: int
    reload: bool

    db: DbConfig = DbConfig()
    api: Api = Api()
    cors_origin_regex: str = r"(http://|https://)?(.*\.)?(qa|stage|localhost|0.0.0.0)" r"(\.ru)?(:\d+)?$"
    # environment: Environments = Environments.local
    # SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_file=find_dotenv(".env"),
    )


APP_CONFIG = AppConfig()  # type: ignore
