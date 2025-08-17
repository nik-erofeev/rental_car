import importlib
import logging
import sys

from colorama import Fore, Style

DEFAULT_LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s"  # noqa: E501 : ignore
# DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

#
# def configure_logging(level: int = logging.INFO) -> None:
#     logging.basicConfig(
#         level=level,
#         datefmt="%Y-%m-%d %H:%M:%S",
#         format=DEFAULT_LOG_FORMAT,
#     )


class ColoredFormatter(logging.Formatter):
    """Форматтер для цветного вывода в консоль."""

    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def __init__(self, fmt=None, datefmt=None, style="%", use_color=True):
        super().__init__(fmt, datefmt, style)
        self.use_color = use_color

    def format(self, record):
        if self.use_color and record.levelno in self.COLORS:
            color = self.COLORS[record.levelno]
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


def configure_logging(
    use_color: bool,
    level: int = logging.INFO,
    enable_http_logs: bool = True,
) -> None:
    """
    Настройка логирования с цветным консольным выводом и JSON-логами для Elastic.

    В консоль всегда выводятся логи в текстовом формате:
        - с цветом, если use_color=True,
        - без цвета, если use_color=False.

    JSON-логи отправляются в отдельный файл для Elastic (через Filebeat).

    :param use_color: Включить цветной вывод в консоль (True) или нет (False).
    :param level: Уровень логирования (по умолчанию INFO).
    :param enable_http_logs: Включить логи HTTP запросов (по умолчанию True).

    Примеры использования:
        configure_logging(use_color=True)   # Цветная консоль + JSON для Elastic
        configure_logging(use_color=False)  # Обычная консоль + JSON для Elastic
    """

    # Настраиваем корневой логгер ТОЛЬКО для консоли
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Консольный вывод (цветной или обычный)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        ColoredFormatter(
            DEFAULT_LOG_FORMAT,
            use_color=use_color,
        ),
    )
    root_logger.addHandler(console_handler)

    # Создаем ОТДЕЛЬНЫЙ логгер для JSON логов в Elastic
    # Этот логгер НЕ будет дублировать логи в консоль
    json_logger = logging.getLogger("elastic_logger")
    json_logger.setLevel(level)
    json_logger.propagate = False  # Отключаем пропагацию в корневой логгер

    try:
        jsonlogger_module = importlib.import_module("pythonjsonlogger.jsonlogger")
        # JSON логи идут в stderr (отдельно от консоли)
        json_handler = logging.StreamHandler(sys.stderr)
        json_formatter = jsonlogger_module.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        json_handler.setFormatter(json_formatter)
        json_logger.addHandler(json_handler)
    except Exception as e:
        logging.getLogger(__name__).error(
            f"Ошибка при настройке JSON логгера для Elastic: {e}",
        )

    # Настраиваем Uvicorn логгер, чтобы избежать дублирования
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()
    uvicorn_logger.propagate = False  # Отключаем пропагацию в корневой логгер

    # Добавляем наш обработчик для Uvicorn
    uvicorn_handler = logging.StreamHandler(sys.stdout)
    uvicorn_handler.setFormatter(
        ColoredFormatter(
            DEFAULT_LOG_FORMAT,
            use_color=use_color,
        ),
    )
    uvicorn_logger.addHandler(uvicorn_handler)

    # Настраиваем FastAPI логгер
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.handlers.clear()
    fastapi_logger.propagate = False

    fastapi_handler = logging.StreamHandler(sys.stdout)
    fastapi_handler.setFormatter(
        ColoredFormatter(
            DEFAULT_LOG_FORMAT,
            use_color=use_color,
        ),
    )
    fastapi_logger.addHandler(fastapi_handler)

    # Настраиваем HTTP логгер (для запросов) - опционально
    if enable_http_logs:
        http_logger = logging.getLogger("uvicorn.access")
        http_logger.handlers.clear()
        http_logger.propagate = False

        http_handler = logging.StreamHandler(sys.stdout)
        http_handler.setFormatter(
            ColoredFormatter(
                DEFAULT_LOG_FORMAT,
                use_color=use_color,
            ),
        )
        http_logger.addHandler(http_handler)
    else:
        # Отключаем HTTP логи полностью
        http_logger = logging.getLogger("uvicorn.access")
        http_logger.disabled = True
        http_logger.propagate = False

    # Настраиваем httptools логгер (для HTTP запросов)
    httptools_logger = logging.getLogger("uvicorn.error")
    httptools_logger.handlers.clear()
    httptools_logger.propagate = False

    httptools_handler = logging.StreamHandler(sys.stdout)
    httptools_handler.setFormatter(
        ColoredFormatter(
            DEFAULT_LOG_FORMAT,
            use_color=use_color,
        ),
    )
    httptools_logger.addHandler(httptools_handler)


def get_elastic_logger() -> logging.Logger:
    """
    Возвращает логгер для отправки логов в Elastic.
    Используйте этот логгер для логирования, которое должно попасть в Grafana.
    """
    return logging.getLogger("elastic_logger")


def disable_http_logs() -> None:
    """Отключает логи HTTP запросов (uvicorn.access)."""
    http_logger = logging.getLogger("uvicorn.access")
    http_logger.disabled = True
    http_logger.propagate = False
