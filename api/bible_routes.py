# api/bible_routes.py
# Эндпоинты для WebApp — список книг, глав, текста Библии (загружается по ссылке)

from fastapi import APIRouter, HTTPException, Query
from typing import List
import json
import requests

BIBLE_URL = "https://github.com/IvanZakhvatkin/biblebot-api/releases/download/v1.0.0/bible-text.json"

router = APIRouter()

# Загрузка текста Библии по HTTP
try:
    response = requests.get(BIBLE_URL)
    response.raise_for_status()
    bible_data = response.json()

    if not isinstance(bible_data, list):
        raise ValueError("❌ Ожидался список, но получен другой тип")
    if not all(isinstance(entry, dict) for entry in bible_data):
        raise ValueError("❌ Один или несколько элементов не являются словарями")

except Exception as e:
    print(f"Ошибка при загрузке Bible JSON с GitHub: {e}")
    bible_data = []

# Индексация
book_chapter_map = {}
book_set = set()

for entry in bible_data:
    book = entry.get("book")
    chapter = entry.get("chapter")
    if book and chapter:
        book_set.add(book)
        book_chapter_map.setdefault(book, set()).add(chapter)

@router.get("/books", response_model=List[str])
def get_books():
    """Список всех книг Библии"""
    return sorted(book_set)

@router.get("/chapters", response_model=List[int])
def get_chapters(book: str = Query(..., description="Название книги")):
    """Список глав в указанной книге"""
    chapters = book_chapter_map.get(book)
    if not chapters:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return sorted(chapters)

@router.get("/bible")
def get_chapter_text(book: str = Query(...), chapter: int = Query(...)):
    """Получить текст указанной главы"""
    for entry in bible_data:
        if entry.get("book") == book and entry.get("chapter") == chapter:
            return {
                "book": book,
                "chapter": chapter,
                "verses": entry.get("verses", [])
            }
    raise HTTPException(status_code=404, detail="Глава не найдена")
