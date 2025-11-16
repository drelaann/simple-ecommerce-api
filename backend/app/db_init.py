"""
Скрипт для инициализации базы данных.
Создает все таблицы на основе моделей.
"""
from app.database import engine, Base
from app.models import User, Product  # Импорт моделей для создания таблиц


def init_db():
    """Создать все таблицы в базе данных."""
    Base.metadata.create_all(bind=engine)
    print("База данных инициализирована успешно!")


if __name__ == "__main__":
    init_db()

