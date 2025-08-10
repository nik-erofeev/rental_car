#!/bin/sh
set -e

# Скрипт создаёт Data View в Kibana при старте окружения
# Имя Data View: rental_car_api_beckend
# Шаблон индекса: filebeat-*
# Поле времени: @timestamp

KIBANA_URL=${KIBANA_URL:-http://kibana:5601}
DATA_VIEW_NAME=${DATA_VIEW_NAME:-rental_car_api_beckend}
DATA_VIEW_TITLE=${DATA_VIEW_TITLE:-filebeat-*}
TIME_FIELD=${TIME_FIELD:-@timestamp}

echo "[kibana_setup] Ожидаю доступность Kibana по $KIBANA_URL ..."
for i in $(seq 1 90); do
  STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$KIBANA_URL/api/status" || true)
  if [ "$STATUS_CODE" = "200" ]; then
    echo "[kibana_setup] Kibana доступна"
    break
  fi
  sleep 2
done

echo "[kibana_setup] Проверяю наличие Data View '$DATA_VIEW_NAME'..."
LIST_JSON=$(curl -s -H 'kbn-xsrf: true' "$KIBANA_URL/api/data_views/list" || true)
echo "$LIST_JSON" | grep -q '"name":"'"$DATA_VIEW_NAME"'"' && {
  echo "[kibana_setup] Data View уже существует. Пропускаю создание."
  exit 0
}

echo "[kibana_setup] Создаю Data View '$DATA_VIEW_NAME'..."
CREATE_PAYLOAD=$(cat <<JSON
{ "data_view": { "title": "$DATA_VIEW_TITLE", "name": "$DATA_VIEW_NAME", "timeFieldName": "$TIME_FIELD" } }
JSON
)

HTTP_CODE=$(curl -s -o /tmp/kibana_create_resp.json -w "%{http_code}" \
  -X POST "$KIBANA_URL/api/data_views/data_view" \
  -H 'kbn-xsrf: true' -H 'Content-Type: application/json' \
  -d "$CREATE_PAYLOAD" || true)

echo "[kibana_setup] HTTP_CODE=$HTTP_CODE"
cat /tmp/kibana_create_resp.json || true

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
  echo "[kibana_setup] Data View успешно создан."
  exit 0
fi

echo "[kibana_setup] Не удалось создать Data View (HTTP $HTTP_CODE). Завершаю без ошибки."
exit 0


