import importlib
import logging

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
) -> None:
    """
    Настройка логирования с цветным консольным выводом и JSON-логами для Elastic.

    В консоль всегда выводятся логи в текстовом формате:
        - с цветом, если use_color=True,
        - без цвета, если use_color=False.

    Кроме того, добавляется JSON-логгер для отправки логов в Elastic (через Filebeat).

    :param use_color: Включить цветной вывод в консоль (True) или нет (False).
    :param level: Уровень логирования (по умолчанию INFO).

    Примеры использования:
        configure_logging(use_color=True)   # Цветная консоль + JSON для Elastic
        configure_logging(use_color=False)  # Обычная консоль + JSON для Elastic
    """

    logger = logging.getLogger()
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Консольный вывод (цветной или обычный)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(DEFAULT_LOG_FORMAT, use_color=use_color))
    logger.addHandler(console_handler)

    # JSON-логи для Elastic (Filebeat)
    try:
        jsonlogger_module = importlib.import_module("pythonjsonlogger.jsonlogger")
        json_handler = logging.StreamHandler()
        # Чистый JSON без форматирования строки
        json_handler.setFormatter(jsonlogger_module.JsonFormatter())
        logger.addHandler(json_handler)
    except Exception as e:
        logging.getLogger(__name__).error(
            f"Ошибка при настройке JSON логгера для Elastic: {e}",
        )
