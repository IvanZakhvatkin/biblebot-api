# api/routes.py — маршруты FastAPI для чтений
# содержит маршруты для получения чтений по дате и списка доступных планов

from fastapi import APIRouter, Query
from api.db import get_db_session
from api.models import ReadingPlan
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional

router = APIRouter()


@router.get("/plan")
def get_plan(date: str, plan: Optional[str] = Query(default=None)):
    """
    Возвращает чтения на заданную дату и план.
    Если параметр plan не указан — используется текущий год.
    """
    plan_name = plan or "plan_" + str(datetime.now().year)

    with next(get_db_session()) as session:
        readings = (
            session.query(ReadingPlan)
            .filter_by(date=date, plan_name=plan_name)
            .all()
        )
        if not readings:
            return {"readings": []}
        return {"readings": [r.to_dict() for r in readings]}


@router.get("/plans")
def get_all_plan_names():
    """
    Возвращает список всех уникальных имён планов (plan_name).
    """
    with next(get_db_session()) as session:
        plan_names = session.query(ReadingPlan.plan_name).distinct().all()
        names = [row[0] for row in plan_names]
        return {"plans": names}
