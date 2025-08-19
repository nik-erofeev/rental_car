
FROM python:3.12-slim


WORKDIR /app

# Установка системных зависимостей
# curl нужен для health checks и HTTP запросов
# apt-get clean удаляет кэш пакетов для уменьшения размера образа
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml uv.lock ./


# Альтернатива: можно использовать pip install -r requirements.txt
RUN pip install uv


RUN uv pip install --system -e .


COPY fs_subscriber/app ./fs_subscriber/app


COPY fs_subscriber/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Документируем, что контейнер слушает на порту 8081
# Это ТОЛЬКО документация для разработчика
# Реальное открытие порта происходит в docker-compose.yml через "ports:"
EXPOSE 8081

# Точка входа - скрипт, который ВСЕГДА выполняется при запуске контейнера
# Аргументы командной строки передаются в entrypoint скрипт как $1, $2, ...
# Например: docker run image docs -> $1 = "docs"
ENTRYPOINT ["/app/entrypoint.sh"]

# Значение по умолчанию для entrypoint скрипта
# Если не указан аргумент, запускается "broker"
# Можно переопределить при запуске: docker run image docs
# Или в docker-compose.yml: command: ["docs"]
CMD ["broker"]
