BEGIN;

-- пароль для всех пользователей: "password" (bcrypt)
INSERT INTO users (email, is_active, full_name, phone, role, hashed_password) VALUES
('user1@example.com',  true, 'User One',   '+79990000001', 'customer', '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user2@example.com',  true, 'User Two',   '+79990000002', 'manager',  '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user3@example.com',  true, 'User Three', '+79990000003', 'admin',    '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user4@example.com',  true, 'User Four',  '+79990000004', 'customer', '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user5@example.com',  true, 'User Five',  '+79990000005', 'manager',  '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user6@example.com',  true, 'User Six',   '+79990000006', 'customer', '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user7@example.com',  true, 'User Seven', '+79990000007', 'manager',  '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user8@example.com',  true, 'User Eight', '+79990000008', 'admin',    '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user9@example.com',  true, 'User Nine',  '+79990000009', 'customer', '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO'),
('user10@example.com', true, 'User Ten',   '+79990000010', 'manager',  '$2b$12$RwN8/Dpz9YqpRL4Ixqbxo.4HKH/MaIB3gFhlpRViS.BxI6Aye3DmO')
ON CONFLICT (email) DO NOTHING;

-- cars
INSERT INTO cars (vin, make, model, year, mileage, price, condition, color, engine_type, transmission, status, description) VALUES
('VIN00000000000001', 'Toyota', 'Corolla', 2019, 40000,  9500.00, 'used',  'white',  'gasoline', 'automatic', 'available', 'Desc 1'),
('VIN00000000000002', 'BMW',    '3 Series',2020, 20000, 20500.00, 'used',  'black',  'diesel',   'automatic', 'reserved',  'Desc 2'),
('VIN00000000000003', 'Audi',   'A4',      2018, 55000, 14500.00, 'used',  'blue',   'gasoline', 'manual',    'available', 'Desc 3'),
('VIN00000000000004', 'Tesla',  'Model 3', 2022, 10000, 32000.00, 'new',   'red',    'electric', 'automatic', 'available', 'Desc 4'),
('VIN00000000000005', 'Honda',  'Civic',   2017, 70000,  8000.00, 'used',  'silver', 'gasoline', 'cvt',       'sold',      'Desc 5'),
('VIN00000000000006', 'Kia',    'Rio',     2021, 15000, 11000.00, 'used',  'white',  'gasoline', 'automatic', 'available', 'Desc 6'),
('VIN00000000000007', 'Ford',   'Focus',   2016, 90000,  6000.00, 'used',  'gray',   'diesel',   'manual',    'available', 'Desc 7'),
('VIN00000000000008', 'Hyundai','Elantra', 2019, 35000,  9900.00, 'used',  'blue',   'gasoline', 'automatic', 'reserved',  'Desc 8'),
('VIN00000000000009', 'VW',     'Golf',    2018, 60000,  8800.00, 'used',  'green',  'diesel',   'manual',    'available', 'Desc 9'),
('VIN00000000000010', 'Nissan', 'Leaf',    2020, 25000, 15000.00, 'used',  'white',  'electric', 'automatic', 'available', 'Desc 10')
ON CONFLICT (vin) DO NOTHING;

-- car_photos
INSERT INTO car_photos (car_id, url, is_main) VALUES
(1,  'https://img.example.com/cars/1-1.jpg',  true),
(2,  'https://img.example.com/cars/2-1.jpg',  true),
(3,  'https://img.example.com/cars/3-1.jpg',  true),
(4,  'https://img.example.com/cars/4-1.jpg',  true),
(5,  'https://img.example.com/cars/5-1.jpg',  true),
(6,  'https://img.example.com/cars/6-1.jpg',  true),
(7,  'https://img.example.com/cars/7-1.jpg',  true),
(8,  'https://img.example.com/cars/8-1.jpg',  true),
(9,  'https://img.example.com/cars/9-1.jpg',  true),
(10, 'https://img.example.com/cars/10-1.jpg', true)
ON CONFLICT DO NOTHING;

-- car_reports
INSERT INTO car_reports (car_id, report_type, data) VALUES
(1,  'vin_check',            '{"score": 92, "notes":"ok"}'),
(2,  'technical_inspection', '{"brakes": "ok", "tires": "worn"}'),
(3,  'vin_check',            '{"score": 85}'),
(4,  'technical_inspection', '{"battery": "new"}'),
(5,  'vin_check',            '{"score": 77}'),
(6,  'vin_check',            '{"score": 88}'),
(7,  'technical_inspection', '{"engine": "leaks"}'),
(8,  'vin_check',            '{"score": 90}'),
(9,  'technical_inspection', '{"suspension": "ok"}'),
(10, 'vin_check',            '{"score": 95}')
ON CONFLICT DO NOTHING;

-- orders
INSERT INTO orders (customer_name, customer_phone, customer_email, user_id, car_id, status, payment_method, total_amount, delivery_address, delivery_date) VALUES
('Buyer 1',  '+79991111111', 'buyer1@example.com',  1,  1, 'pending',     'cash',  15000.00, 'Addr 1', now() + interval '3 days'),
('Buyer 2',  '+79992222222', 'buyer2@example.com',  2,  2, 'paid',        'card',  20500.00, 'Addr 2', now() + interval '2 days'),
('Buyer 3',  '+79993333333', 'buyer3@example.com',  3,  3, 'processing',  'loan',  14500.00, 'Addr 3', now() + interval '4 days'),
('Buyer 4',  '+79994444444', 'buyer4@example.com',  4,  4, 'in_delivery', 'lease', 32000.00, 'Addr 4', now() + interval '1 days'),
('Buyer 5',  '+79995555555', 'buyer5@example.com',  5,  5, 'completed',   'cash',   8000.00, 'Addr 5', now() - interval '1 days'),
('Buyer 6',  '+79996666666', 'buyer6@example.com',  6,  6, 'pending',     'card',  11000.00, 'Addr 6', now() + interval '5 days'),
('Buyer 7',  '+79997777777', 'buyer7@example.com',  7,  7, 'canceled',    'loan',   6000.00, 'Addr 7', now() + interval '7 days'),
('Buyer 8',  '+79998888888', 'buyer8@example.com',  8,  8, 'processing',  'lease',  9900.00, 'Addr 8', now() + interval '6 days'),
('Buyer 9',  '+79999999999', 'buyer9@example.com',  9,  9, 'paid',        'card',   8800.00, 'Addr 9', now() + interval '3 days'),
('Buyer 10', '+79990000000', 'buyer10@example.com', 10, 10, 'pending',     'cash',  15000.00, 'Addr 10',now() + interval '2 days')
ON CONFLICT DO NOTHING;

-- deliveries
INSERT INTO deliveries (order_id, status, tracking_number, delivered_at) VALUES
(1,  'pending',     'TRK0001', NULL),
(2,  'delivered',   'TRK0002', now()),
(3,  'in_progress', 'TRK0003', NULL),
(4,  'in_progress', 'TRK0004', NULL),
(5,  'delivered',   'TRK0005', now()),
(6,  'pending',     'TRK0006', NULL),
(7,  'failed',      'TRK0007', NULL),
(8,  'in_progress', 'TRK0008', NULL),
(9,  'pending',     'TRK0009', NULL),
(10, 'pending',     'TRK0010', NULL)
ON CONFLICT DO NOTHING;

-- payments
INSERT INTO payments (order_id, amount, status, payment_type, transaction_id, paid_at) VALUES
(1,  15000.00, 'paid',     'full',        'TXN0001', now()),
(2,  20500.00, 'paid',     'full',        'TXN0002', now()),
(3,  14500.00, 'pending',  'installment', 'TXN0003', NULL),
(4,  32000.00, 'pending',  'installment', 'TXN0004', NULL),
(5,   8000.00, 'paid',     'deposit',     'TXN0005', now()),
(6,  11000.00, 'pending',  'full',        'TXN0006', NULL),
(7,   6000.00, 'failed',   'deposit',     'TXN0007', NULL),
(8,   9900.00, 'pending',  'installment', 'TXN0008', NULL),
(9,   8800.00, 'paid',     'full',        'TXN0009', now()),
(10, 15000.00, 'pending',  'deposit',     'TXN0010', NULL)
ON CONFLICT DO NOTHING;

-- reviews
INSERT INTO reviews (customer_name, user_id, car_id, rating, comment) VALUES
('Rev 1',  1,  1, 5, 'Great car'),
('Rev 2',  2,  2, 4, 'Good'),
('Rev 3',  3,  3, 3, 'Average'),
('Rev 4',  4,  4, 5, 'Excellent'),
('Rev 5',  5,  5, 2, 'Needs work'),
('Rev 6',  6,  6, 4, 'Nice ride'),
('Rev 7',  7,  7, 3, 'Ok'),
('Rev 8',  8,  8, 5, 'Love it'),
('Rev 9',  9,  9, 4, 'Solid'),
('Rev 10', 10, 10, 5, 'Perfect')
ON CONFLICT DO NOTHING;

COMMIT;
