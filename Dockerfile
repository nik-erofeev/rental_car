# syntax=docker/dockerfile:1
FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=10 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONPATH="/app"

WORKDIR /app

# Установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y postgresql-client curl netcat-openbsd && \
    apt-get clean

# Устанавливаем uv через pip
RUN pip install --upgrade pip && pip install uv

# Копируем зависимости для uv
COPY pyproject.toml uv.lock ./

# Ставим зависимости прямо в системный Python контейнера
RUN uv pip install --system --no-cache .

# Копируем исходники
COPY app/ ./app
COPY migrations/ ./migrations
COPY alembic.ini/ ./alembic.ini
COPY ./README.md .

COPY docker /app/docker
RUN chmod +x /app/docker/*


EXPOSE 8000

# указали в docker-compose
#CMD ["/app/docker/app.sh"]
