## Гайд по миграциям

### Бинарь окружения
Запускать Alembic через бинарь venv с абсолютным путём:
```bash
/Users/Nik/Desktop/my_test_project/rental_car/.venv/bin/alembic revision --autogenerate -m "Описание изменений"
/Users/Nik/Desktop/my_test_project/rental_car/.venv/bin/alembic upgrade head
```

### Target metadata и импорты моделей
- `migrations/env.py` использует `target_metadata = app.models.Base.metadata`.
- Все модели должны быть импортированы в `app/models/__init__.py`.

### PostgreSQL ENUM (принятая политика)
- В моделях отключаем автосоздание типа (`create_type=False`) и задаём имя типа:
  ```python
  from sqlalchemy.dialects.postgresql import ENUM as PGEnum
  role: Mapped[UserRole] = mapped_column(PGEnum('customer', 'manager', 'admin', name='user_role', create_type=False))
  ```
- Создание типов — руками (отдельная миграция или явный SQL):
  ```python
  op.execute("CREATE TYPE IF NOT EXISTS user_role AS ENUM ('customer','manager','admin');")
  ```
- Добавление колонки с ENUM — без автосоздания типа, предполагается, что тип уже есть:
  ```python
  op.add_column('users', sa.Column('role', sa.Enum('customer','manager','admin', name='user_role', create_type=False), nullable=False))
  ```
- Удаление типов — руками, когда они больше нигде не используются:
  ```python
  # todo: для ENUM руками-алембик не удаляет
  op.execute("DROP TYPE IF EXISTS user_role CASCADE;")
  op.execute("DROP TYPE IF EXISTS car_condition CASCADE;")
  op.execute("DROP TYPE IF EXISTS engine_type CASCADE;")
  op.execute("DROP TYPE IF EXISTS transmission CASCADE;")
  op.execute("DROP TYPE IF EXISTS car_status CASCADE;")
  op.execute("DROP TYPE IF EXISTS order_status CASCADE;")
  op.execute("DROP TYPE IF EXISTS payment_method CASCADE;")
  op.execute("DROP TYPE IF EXISTS delivery_status CASCADE;")
  op.execute("DROP TYPE IF EXISTS payment_status CASCADE;")
  op.execute("DROP TYPE IF EXISTS payment_type CASCADE;")
  ```

### SQLite
- Для совместимости можно указывать `create_constraint=True, validate_strings=True` в `Enum(...)` (создаст CHECK вместо ENUM).

### Частые ошибки
- `type "<enum>" does not exist` — добавьте явное `create()` типа перед `add_column`.
- Alembic не видит таблицу — проверьте импорт модели в `app/models/__init__.py` и `target_metadata`.


