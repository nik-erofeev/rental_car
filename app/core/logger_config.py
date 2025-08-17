import logging
import sys

from colorama import Fore, Style

DEFAULT_LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(funcName)20s %(module)s:%(lineno)d %(levelname)-8s - %(message)s"  # noqa: E501 : ignore


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


def _setup_logger(
    name: str,
    level: int,
    formatter: logging.Formatter,
    stream=sys.stdout,
    propagate: bool = False,
) -> logging.Logger:
    """Вспомогательная функция для настройки логгера."""
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = propagate
    
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger


def configure_logging(
    use_color: bool,
    level: int = logging.INFO,
    enable_http_logs: bool = True,
) -> None:
    """
    Настройка логирования с цветным консольным выводом и JSON-логами для Elastic.

    :param use_color: Включить цветной вывод в консоль
    :param level: Уровень логирования
    :param enable_http_logs: Включить логи HTTP запросов
    """

    # Очищаем корневой логгер
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Создаем форматтеры
    console_formatter = ColoredFormatter(DEFAULT_LOG_FORMAT, use_color=use_color)
    
    # Настраиваем корневой логгер (консоль)
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setFormatter(console_formatter)
    root_logger.addHandler(root_handler)

    # Настраиваем JSON логгер для Elastic (stderr)
    try:
        from pythonjsonlogger import json
        
        json_formatter = json.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        _setup_logger(
            "elastic_logger", level, json_formatter, sys.stderr, propagate=False
        )
        
    except ImportError:
        logging.getLogger(__name__).error("python-json-logger не установлен")

    # Настраиваем все остальные логгеры
    loggers_to_setup = [
        ("uvicorn", True),
        ("fastapi", True),
        ("uvicorn.access", enable_http_logs),
        ("uvicorn.error", True),
    ]

    for logger_name, should_enable in loggers_to_setup:
        if should_enable:
            _setup_logger(
                logger_name, level, console_formatter, sys.stdout, propagate=False
            )
        else:
            logger = logging.getLogger(logger_name)
            logger.disabled = True
            logger.propagate = False


def get_elastic_logger() -> logging.Logger:
    """Возвращает логгер для отправки логов в Elastic."""
    return logging.getLogger("elastic_logger")


def disable_http_logs() -> None:
    """Отключает логи HTTP запросов."""
    logger = logging.getLogger("uvicorn.access")
    logger.disabled = True
    logger.propagate = False
