# api/bible_routes.py

from fastapi import APIRouter, HTTPException, Query
from typing import List
import json
import requests

BIBLE_URL = "https://github.com/IvanZakhvatkin/biblebot-api/releases/download/v1.0.0/bible-text.json"

router = APIRouter()

# Загрузка Библии по HTTP (с авто-редиректом и заголовком)
try:
    response = requests.get(BIBLE_URL, headers={"User-Agent": "BibleBot"}, allow_redirects=True)
    response.raise_for_status()

    try:
        bible_data = response.json()
    except json.JSONDecodeError:
        raise ValueError("❌ Ответ не является корректным JSON")

    if not isinstance(bible_data, list):
        raise ValueError("❌ Ожидался список, но получен другой тип")

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
    return sorted(book_set)

@router.get("/chapters", response_model=List[int])
def get_chapters(book: str = Query(...)):
    chapters = book_chapter_map.get(book)
    if not chapters:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return sorted(chapters)

@router.get("/bible")
def get_chapter_text(book: str = Query(...), chapter: int = Query(...)):
    for entry in bible_data:
        if entry.get("book") == book and entry.get("chapter") == chapter:
            return {
                "book": book,
                "chapter": chapter,
                "verses": entry.get("verses", [])
            }
    raise HTTPException(status_code=404, detail="Глава не найдена")
