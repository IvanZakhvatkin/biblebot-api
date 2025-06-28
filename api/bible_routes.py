# web_app/api/bible_routes.py
# Эндпоинты для WebApp — список книг, глав, текста Библии

from fastapi import APIRouter, HTTPException, Query
from typing import List
import json
from api.config import BIBLE_PATH

router = APIRouter()

# Загрузка и кэширование текста Библии
try:
    with open(BIBLE_PATH, encoding="utf-8") as f:
        bible_data = json.load(f)
except Exception as e:
    print(f"Ошибка при загрузке Bible JSON: {e}")
    bible_data = []

# Строим вспомогательные индексы
book_chapter_map = {}
book_set = set()

for entry in bible_data:
    book = entry["book"]
    chapter = entry["chapter"]
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
        if entry["book"] == book and entry["chapter"] == chapter:
            return {
                "book": book,
                "chapter": chapter,
                "verses": entry["verses"]
            }
    raise HTTPException(status_code=404, detail="Глава не найдена")
