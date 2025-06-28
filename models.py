# api/models.py
# Модели таблиц: users, progress, reading_plan, admins

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date)
    settings = Column(String)


class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"))
    date = Column(Date)
    chapter = Column(String)
    status = Column(Boolean, default=False)


class ReadingPlan(Base):
    __tablename__ = "reading_plan"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    keys = Column(String, nullable=False)
    plan_name = Column(String, nullable=False,
                       default="default")  # Добавлено поле

    def to_dict(self):
        return {
            "id": self.id,
            "date": str(self.date),
            "keys": self.keys,
            "plan_name": self.plan_name,
        }


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True)
