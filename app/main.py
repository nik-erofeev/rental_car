import logging

from app.application import create_app
from app.core.logger_config import configure_logging
from app.core.settings import APP_CONFIG
import uvicorn

# Настройка логирования
configure_logging()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Глобальный логгер для всего приложения

app = create_app(APP_CONFIG)


if __name__ == "__main__":
    logger.info("🚀 Запуск FastAPI приложения...")

    try:
        uvicorn.run(
            "app.main:app",
            host=APP_CONFIG.app_host,
            port=APP_CONFIG.app_port,
            reload=APP_CONFIG.reload,
            workers=APP_CONFIG.workers,
        )
    except KeyboardInterrupt:
        logger.info("🛑 Приложение остановлено пользователем (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка при запуске: {e}")
    finally:
        logger.info("✅ Приложение завершено")
