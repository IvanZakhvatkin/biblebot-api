# api/load_plan.py
# Скрипт импорта плана чтения в базу данных
# Использует SQLAlchemy для работы с базой данных
# Читает JSON-файл с планом чтения и сохраняет его в табли


import os
import json
from datetime import datetime
from sqlalchemy.orm import Session
from api.database import SessionLocal
from api.models import ReadingPlan

# Папка, где хранятся все планы
PLANS_DIR = "data/plans"


def load_plan_file(filepath: str, plan_name: str, db: Session):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    for entry in data:
        date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
        readings = entry.get("readings", [])
        keys = "; ".join(readings)  # 🆕 объединяем список в строку
        plan = ReadingPlan(date=date, keys=keys, plan_name=plan_name)
        db.add(plan)

    print(f"✅ Загружен план: {plan_name} ({len(data)} записей)")


def load_all_plans():
    db = SessionLocal()
    try:
        for filename in os.listdir(PLANS_DIR):
            if filename.endswith(".json"):
                plan_name = filename.replace(".json", "")
                filepath = os.path.join(PLANS_DIR, filename)
                load_plan_file(filepath, plan_name, db)
        db.commit()
        print("📘 Все планы успешно загружены в базу данных.")
    finally:
        db.close()


if __name__ == "__main__":
    load_all_plans()
