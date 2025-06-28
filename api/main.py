# api/main.py
# # содержит основной код FastAPI приложения
# # подключает маршруты и инициализирует базу данных

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as plan_router
from api.init_db import init_db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(plan_router)

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000)
