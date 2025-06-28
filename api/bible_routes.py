# api/bible_routes.py
# Эндпоинты для WebApp — загрузка книг Библии с GitHub

from fastapi import APIRouter, HTTPException, Query
from typing import List
import json
import requests

# Папка, где лежат книги в raw.githubusercontent.com
BASE_URL = "https://raw.githubusercontent.com/IvanZakhvatkin/biblebot-api/main/books"

# Статический список книг (можно автоматизировать через GitHub API, но этого достаточно)
BOOK_LIST = [
    "Бытие", "Исход", "Левит", "Числа", "Второзаконие", "Иисус Навин", "Судьи", "Руфь",
    "1 Царств", "2 Царств", "3 Царств", "4 Царств", "1 Паралипоменон", "2 Паралипоменон",
    "Ездра", "Неемия", "Есфирь", "Иов", "Псалтирь", "Притчи", "Экклесиаст", "Песнь Песней",
    "Исаия", "Иеремия", "Плач Иеремии", "Иезекииль", "Даниил", "Осия", "Иоиль", "Амос",
    "Авдий", "Иона", "Михей", "Наум", "Аввакум", "Софония", "Аггей", "Захария", "Малахия",
    "Матфей", "Марка", "Лука", "Иоанн", "Деяния", "Римлянам", "1 Коринфянам", "2 Коринфянам",
    "Галатам", "Ефесянам", "Филиппийцам", "Колоссянам", "1 Фессалоникийцам", "2 Фессалоникийцам",
    "1 Тимофею", "2 Тимофею", "Титу", "Филимону", "Евреям", "Иакова", "1 Петра", "2 Петра",
    "1 Иоанна", "2 Иоанна", "3 Иоанна", "Иуда", "Откровение"
]

router = APIRouter()

def get_book_json(book: str) -> list:
    safe_name = book.replace(" ", "_")
    url = f"{BASE_URL}/{safe_name}.json"

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Некорректный формат главы книги")
        return data
    except Exception as e:
        print(f"❌ Ошибка загрузки книги {book}: {e}")
        raise HTTPException(status_code=404, detail=f"Книга '{book}' не найдена")

@router.get("/books", response_model=List[str])
def get_books():
    """Список всех книг Библии"""
    return BOOK_LIST

@router.get("/chapters", response_model=List[int])
def get_chapters(book: str = Query(..., description="Название книги")):
    """Список глав в указанной книге"""
    data = get_book_json(book)
    return sorted(set(entry["chapter"] for entry in data))

@router.get("/bible")
def get_chapter_text(book: str = Query(...), chapter: int = Query(...)):
    """Получить текст указанной главы"""
    data = get_book_json(book)
    for entry in data:
        if entry.get("chapter") == chapter:
            return {
                "book": book,
                "chapter": chapter,
                "verses": entry.get("verses", [])
            }
    raise HTTPException(status_code=404, detail="Глава не найдена")
