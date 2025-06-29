# api/main.py
# содержит основной код FastAPI приложения
# подключает маршруты и инициализирует базу данных

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as plan_router
from api.bible_routes import router as bible_router
from api.init_db import init_db
from api.load_plan import load_plan_from_file

print("✅ Загрузка FastAPI-приложения")
app = FastAPI()

# Разрешаем CORS для WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде можно ограничить домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS middleware успешно подключён")

# Подключение маршрутов
app.include_router(plan_router)
app.include_router(bible_router)

# 🔧 Временный маршрут для инициализации базы
@app.get("/init")
def initialize():
    try:
        init_db()
        return {"message": "База данных успешно инициализирована ✅"}
    except Exception as e:
        return {"error": str(e)}

# 🔧 Временный маршрут для загрузки плана в базу
@app.get("/load_plan")
def load_plan():
    try:
        load_plan_from_file("data/plans/plan_2025.json", "plan_2025")
        return {"message": "План успешно загружен в базу ✅"}
    except Exception as e:
        return {"error": str(e)}

# Только для локального запуска
if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000)
