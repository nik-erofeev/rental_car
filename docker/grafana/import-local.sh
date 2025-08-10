#!/bin/sh
set -e

apk add --no-cache curl jq >/dev/null 2>&1 || true

if [ -z "$DASHBOARD_PATH" ] || [ ! -f "$DASHBOARD_PATH" ]; then
  echo "Dashboard file not found: $DASHBOARD_PATH" >&2
  exit 1
fi

until curl -sf http://grafana:3000/api/health >/dev/null; do
  echo 'waiting grafana'; sleep 2;
done

jq -n --slurpfile d "$DASHBOARD_PATH" '{
  "dashboard": $d[0],
  "overwrite": true,
  "inputs": [
    {"name":"DS_PROMETHEUS","type":"datasource","pluginId":"prometheus","value":"Prometheus"},
    {"name":"DS_LOKI","type":"datasource","pluginId":"loki","value":"Loki"}
  ]
}' > /tmp/payload.json

curl -sf -u "${GRAFANA_USER:-admin}:${GRAFANA_PASSWORD:-admin}" \
  -H 'Content-Type: application/json' \
  -d @/tmp/payload.json \
  http://grafana:3000/api/dashboards/import && echo 'imported' || echo 'import failed'


