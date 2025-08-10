#!/bin/sh
set -e

# Установка curl и jq (alpine)
apk add --no-cache curl jq >/dev/null 2>&1 || true

# Ожидаем готовность Grafana
until curl -sf http://grafana:3000/api/health >/dev/null; do
  echo "waiting grafana"; sleep 2;
done

# Источник дашборда: локальный файл, который проброшен в контейнер
DASHBOARD_JSON_PATH="/dashboards/16110_rev4.json"
if [ ! -f "$DASHBOARD_JSON_PATH" ]; then
  echo "Dashboard file not found: $DASHBOARD_JSON_PATH" >&2
  exit 1
fi

# Формируем payload с маппингом datasources
jq -n --slurpfile d "$DASHBOARD_JSON_PATH" '{
  dashboard: $d[0],
  overwrite: true,
  inputs: [
    {"name":"DS_PROMETHEUS","type":"datasource","pluginId":"prometheus","value":"Prometheus"},
    {"name":"DS_LOKI","type":"datasource","pluginId":"loki","value":"Loki"}
  ]
}' > /tmp/payload.json

# Импорт через API
curl -sf -u "${GRAFANA_USER:-admin}:${GRAFANA_PASSWORD:-admin}" \
  -H 'Content-Type: application/json' \
  -d @/tmp/payload.json \
  http://grafana:3000/api/dashboards/import && echo 'imported'


