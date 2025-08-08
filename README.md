### Упрощённая модель данных (без авторизации)
1. Автомобили (cars)
id — PK

vin — уникальный

make — марка (Toyota, BMW...)

model — модель

year — год выпуска

mileage — пробег (км)

price — цена

condition — (new, used)

color

engine_type — (gasoline, diesel, hybrid, electric)

transmission — (manual, automatic, cvt)

status — (available, reserved, sold)

description — текстовое описание

created_at

updated_at

2. Фотографии автомобилей (car_photos)
id — PK

car_id — FK → cars.id

url — путь к изображению

is_main — флаг главного фото

3. Заказы (orders)
id — PK

customer_name — имя клиента

customer_phone — телефон

customer_email — email

car_id — FK → cars.id

status — (pending, paid, processing, in_delivery, completed, canceled)

payment_method — (cash, card, loan, lease)

total_amount — сумма

delivery_address

delivery_date — планируемая доставка

created_at

updated_at

4. Доставка (deliveries)
id — PK

order_id — FK → orders.id

status — (pending, in_progress, delivered, failed)

tracking_number

delivered_at

5. Платежи (payments)
id — PK

order_id — FK → orders.id

amount

status — (pending, paid, failed)

payment_type — (full, installment, deposit)

transaction_id — ID транзакции в платёжной системе

paid_at

6. Отчёты по VIN и диагностике (car_reports)
id — PK

car_id — FK → cars.id

report_type — (vin_check, technical_inspection)

data — JSON (результаты проверки)

created_at

7. Отзывы (reviews)
id — PK

customer_name

car_id — FK → cars.id

rating — 1–5

comment

created_at


### ERD-связи

cars ───< car_photos
cars ───< car_reports
cars ───< reviews
cars ───< orders ───< payments
orders ───< deliveries
