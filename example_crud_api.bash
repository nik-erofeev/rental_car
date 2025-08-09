#!/bin/bash

set -euo pipefail


# USERS
# Создать
curl -X POST "http://localhost:8000/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"user1@example.com"}'

# Получить по ID
curl "http://localhost:8000/v1/users/1"

# Список (с фильтром и пагинацией)
curl "http://localhost:8000/v1/users/?is_active=true&limit=20&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/users/1" \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com","is_active":false}'


# # Удалить
# curl -X DELETE "http://localhost:8000/v1/users/1"


# CARS
# Создать
curl -X POST "http://localhost:8000/v1/cars/" \
  -H "Content-Type: application/json" \
  -d '{
    "vin":"JTDBR32E720123456",
    "make":"Toyota",
    "model":"Corolla",
    "year":2020,
    "mileage":45000,
    "price":12500.50,
    "condition":"new",
    "color":"white",
    "engine_type":"gasoline",
    "transmission":"automatic",
    "status":"available",
    "description":"Test car"
  }'

# Получить по ID
curl "http://localhost:8000/v1/cars/1"

# Список
curl "http://localhost:8000/v1/cars/?limit=10&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/cars/1" \
  -H "Content-Type: application/json" \
  -d '{"price":11999.99,"status":"reserved"}'

# Удалить (оставьте закомментированным, если планируете создавать заказы на car_id=1)
# curl -X DELETE "http://localhost:8000/v1/cars/1"


# ORDERS
# Прежде чем создавать заказ, убедитесь, что есть машина и возьмите её id (например, 1).
# Создать
curl -X POST "http://localhost:8000/v1/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name":"Иван Петров",
    "customer_phone":"+79999999999",
    "customer_email":"buyer@example.com",
    "user_id": null,
    "car_id": 1,
    "status":"pending",
    "payment_method":"cash",
    "total_amount": 15000.00,
    "delivery_address":"Москва, ул. Тестовая, д.1"
  }'

# Получить по ID
curl "http://localhost:8000/v1/orders/1"

# Список
curl "http://localhost:8000/v1/orders/?limit=10&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/orders/1" \
  -H "Content-Type: application/json" \
  -d '{"status":"paid","payment_method":"card"}'

# # Удалить
# curl -X DELETE "http://localhost:8000/v1/orders/1"


# Примечания:
# - Для orders: car_id > 0 и должен существовать; при неверном car_id вернётся 404.
# - customer_phone должен быть в формате +7XXXXXXXXXX.
# - delivery_date можно передавать с таймзоной (Z/±hh:mm) — внутри нормализуется.


# PAYMENTS
# Создать
curl -X POST "http://localhost:8000/v1/payments/" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "amount": 15000.00,
    "status": "paid",
    "payment_type": "full",
    "transaction_id": "TXN-DEMO-1"
  }'

# Получить по ID
curl "http://localhost:8000/v1/payments/1"

# Список
curl "http://localhost:8000/v1/payments/?limit=10&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/payments/1" \
  -H "Content-Type: application/json" \
  -d '{"status":"pending","payment_type":"installment"}'

# Удалить
# curl -X DELETE "http://localhost:8000/v1/payments/1"


# DELIVERIES
# Создать
curl -X POST "http://localhost:8000/v1/deliveries/" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "status": "in_progress",
    "tracking_number": "TRK-DEMO-1"
  }'

# Получить по ID
curl "http://localhost:8000/v1/deliveries/1"

# Список
curl "http://localhost:8000/v1/deliveries/?limit=10&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/deliveries/1" \
  -H "Content-Type: application/json" \
  -d '{"status":"delivered","tracking_number":"TRK-DEMO-1"}'

# Удалить
# curl -X DELETE "http://localhost:8000/v1/deliveries/1"


# REVIEWS
# Создать
curl -X POST "http://localhost:8000/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Иван",
    "user_id": 1,
    "car_id": 1,
    "rating": 5,
    "comment": "Отличный автомобиль"
  }'

# Получить по ID
curl "http://localhost:8000/v1/reviews/1"

# Список (по car_id)
curl "http://localhost:8000/v1/reviews/?car_id=1&limit=10&offset=0"

# Обновить
curl -X PUT "http://localhost:8000/v1/reviews/1" \
  -H "Content-Type: application/json" \
  -d '{"rating":4,"comment":"Норм, но есть нюансы"}'

# Удалить
# curl -X DELETE "http://localhost:8000/v1/reviews/1"