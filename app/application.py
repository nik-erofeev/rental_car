import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.api.car_photos.routers import router as car_photos_router
from app.api.car_reports.routers import router as car_reports_router
from app.api.cars.routers import router as cars_router
from app.api.default.routers import router as default_router
from app.api.deliveries.routers import router as deliveries_router
from app.api.orders.routers import router as orders_router
from app.api.payments.routers import router as payments_router
from app.api.reviews.routers import router as reviews_router
from app.api.users.routers import router as users_router
from app.core.logger_config import configure_logging
from app.core.settings import APP_CONFIG, AppConfig

# Настройка логирования
configure_logging()
logger = logging.getLogger(__name__)


def _init_routes(app: FastAPI) -> None:
    """Подключение всех роутеров к приложению.

    Args:
        app: Экземпляр FastAPI, к которому нужно подключить роутеры
    """
    routers = [
        default_router,
        users_router,
        cars_router,
        orders_router,
        payments_router,
        deliveries_router,
        reviews_router,
        car_photos_router,
        car_reports_router,
    ]
    for router in routers:
        app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("🚀 Запуск FastAPI приложения...")
    app.state.database_pool = create_async_engine(
        str(APP_CONFIG.db.sqlalchemy_db_uri),
        echo=APP_CONFIG.db.echo,
    )
    app.state.session_maker = async_sessionmaker(
        app.state.database_pool,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield {}
    logger.info("🛑 Завершение работы приложения...")
    await app.state.database_pool.dispose()
    logger.info("✅ Приложение остановлено.")


def create_app(config: AppConfig) -> FastAPI:
    """
    Создание и конфигурация FastAPI приложения.

    Returns:
        Сконфигурированное приложение FastAPI
    """
    app_ = FastAPI(
        title=config.api.project_name,
        description=config.api.description,
        version=config.api.version,
        contact={"name": "Nik", "email": "example@example.com"},
        openapi_url=config.api.openapi_url,
        debug=config.api.echo,
        lifespan=lifespan,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origin_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # эндпоинт для отображения метрик для их дальнейшего сбора Прометеусом
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        excluded_handlers=[".*admin.*", "/metrics"],
    )
    instrumentator.instrument(app_).expose(
        app_,
        include_in_schema=True,
    )  # можно выкл

    _init_routes(app_)

    @app_.exception_handler(Exception)
    async def http_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.error(f"❌An unexpected error occurred: {exc=!r}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred"},
        )

    @app_.get("/")
    def root():
        return {"message": "Rental_Car API 🚀"}

    return app_
