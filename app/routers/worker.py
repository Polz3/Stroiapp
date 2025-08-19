# app/routers/worker.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.api.auth import get_current_user
from app.models.models import User
from app import crud

router = APIRouter()

@router.get("/workers/{worker_id}/card", response_class=HTMLResponse, name="pages.worker_card")
def worker_detail(
    request: Request,
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    worker = crud.worker.get_worker(db=db, worker_id=worker_id, user_id=current_user.id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    # Все зарплаты пользователя -> фильтруем по сотруднику
    salaries = crud.salary.get_salaries(db=db, user_id=current_user.id)
    worker_salaries = [s for s in salaries if s.worker_id == worker_id]

    # JSON-данные для графика (только простые типы!)
    salaries_json = [{"amount": float(s.amount), "date": str(s.date)} for s in worker_salaries]

    # Если у вас нет связи worker.sites — эти две строки можно убрать или позже донастроить
    active_sites = []
    archived_sites = []

    return request.app.state.templates.TemplateResponse(
        "worker_detail.html",
        {
            "request": request,
            "worker": worker,
            "salaries": worker_salaries,
            "salaries_json": salaries_json,  # ← ВАЖНО: передаём!
            "active_sites": active_sites,
            "archived_sites": archived_sites,
        },
    )
