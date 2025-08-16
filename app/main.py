import sentry_sdk
import uvicorn

from app.application import create_app
from app.core.settings import APP_CONFIG

if APP_CONFIG.sentry_dsn:
    sentry_sdk.init(dsn=str(APP_CONFIG.sentry_dsn), enable_tracing=True, send_default_pii=True)

app = create_app(APP_CONFIG)


# todo: поправить ошибку - вынести ошибку при отправке в кавку
# todo: разобраться с дублирование логов в консоль
if __name__ == "__main__":
    # что бы работала остановка: cmd+c. Запускать :
    # uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    uvicorn.run(
        "app.main:app",
        host=APP_CONFIG.app_host,
        port=APP_CONFIG.app_port,
        reload=APP_CONFIG.reload,
        workers=APP_CONFIG.workers,
        log_config=None,  # Чтобы не переопределял логгер
    )
