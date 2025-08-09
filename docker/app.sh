#!/bin/sh

# export env
POSTGRES_HOST=${DB__HOST}
POSTGRES_PORT=${DB__PORT}

echo "Waiting for PostgreSQL to start..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done


echo "Starting migrations..."
alembic upgrade head

echo Check migration status
MIGRATION_STATUS=$?
if [ $MIGRATION_STATUS -ne 0 ]; then
  echo "Migrations failed with status $MIGRATION_STATUS"
  exit 1
fi

# Заливаем тестовые данные
if [ -f /app/docker/example_sql.sql ]; then
  echo "Seeding database with example data..."
  psql "postgresql://${DB__USER}:${DB__PASSWORD}@${DB__HOST}:${DB__PORT}/${DB__NAME}" \
    -f /app/docker/example_sql.sql
  SEED_STATUS=$?
  if [ $SEED_STATUS -ne 0 ]; then
    echo "Seeding failed with status $SEED_STATUS"
    exit 1
  fi
else
  echo "No seed file found, skipping..."
fi


echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000