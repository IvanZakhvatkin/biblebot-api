# api/init_db.py
# создание таблиц

from .database import engine
from .models import Base


def init_db():
    Base.metadata.create_all(bind=engine)
    print("📘 База данных и таблицы успешно созданы.")


# Эта строка нужна, чтобы код сработал при запуске через python -m
if __name__ == "__main__":
    init_db()
