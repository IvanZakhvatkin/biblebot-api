# api/config.py
# получает переменные из .env (TOKEN, USERNAME, DB, BIBLE_PATH)

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bible.db")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Путь к файлу с текстом Библии
BIBLE_PATH = os.getenv("BIBLE_PATH", os.path.join("data", "bible-text.json"))

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")

if not BOT_USERNAME:
    raise ValueError("❌ BOT_USERNAME не найден в .env")
