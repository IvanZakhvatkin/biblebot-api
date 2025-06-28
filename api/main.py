# api/main.py
# содержит основной код FastAPI приложения
# подключает маршруты и инициализирует базу данных

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as plan_router
from api.bible_routes import router as bible_router  # теперь из api/
from api.init_db import init_db

print("✅ Загрузка FastAPI-приложения")
app = FastAPI()

# Разрешаем CORS для WebApp
app.add_middleware(
    CORSMiddleware,
    # можно заменить на конкретный домен WebApp в продакшене
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS middleware успешно подключён")

# Подключение маршрутов
app.include_router(plan_router)
app.include_router(bible_router)

# Только для локального запуска
if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000)
