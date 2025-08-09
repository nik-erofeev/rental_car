import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import AppConfig, APP_CONFIG
from app.api.users.routers import router as users_router


from app.api.default.routers import router as default_router
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    logger.info("Инициализация приложения...")
    app.state.database_pool = create_async_engine(
        str(APP_CONFIG.db.sqlalchemy_db_uri),
        echo=APP_CONFIG.db.echo,
    )
    app.state.session_maker = async_sessionmaker(
        app.state.database_pool,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield
    logger.info("Завершение работы приложения...")
    await app.state.database_pool.dispose()


def create_app(config: AppConfig) -> FastAPI:
    """
    Создание и конфигурация FastAPI приложения.

    Returns:
        Сконфигурированное приложение FastAPI
    """
    app = FastAPI(
        title=config.api.project_name,
        description=config.api.description,
        version=config.api.version,
        contact={"name": "Nik", "email": "example@example.com"},
        openapi_url=config.api.openapi_url,
        debug=config.api.echo,
        lifespan=lifespan,
    )

    app.add_middleware(
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
    instrumentator.instrument(app).expose(app, include_in_schema=True)  # можно выкл

    app.include_router(default_router)
    app.include_router(users_router)

    @app.exception_handler(Exception)
    async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"An unexpected error occurred: {exc=!r}")
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred"},
        )

    @app.get("/")
    def root():
        return {"message": "Rental_Car API 🚀"}

    return app
