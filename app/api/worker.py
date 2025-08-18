# app/api/worker.py
from fastapi import APIRouter, Depends, HTTPException, Body, Form
from sqlalchemy.orm import Session

from app.database.db import get_db
import app.crud.worker as crud_worker
from app.api.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import WorkerCreate, Worker as WorkerOut

router = APIRouter(prefix="/api/workers", tags=["workers"])

# --- Список сотрудников ---
@router.get("")
@router.get("/", response_model=list[WorkerOut])
def read_workers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_worker.get_workers(db, user_id=current_user.id)

# --- Получить одного сотрудника ---
@router.get("/{worker_id}", response_model=WorkerOut)
def read_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    w = crud_worker.get_worker(db, worker_id)
    if not w or w.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Worker not found")
    return w

# --- Создать сотрудника (поддержка JSON и form-data) ---
@router.post("")
@router.post("/", response_model=WorkerOut)
def create_worker(
    payload: WorkerCreate | None = Body(default=None),
    # альтернативный путь: если придёт form-data вместо JSON
    name: str | None = Form(default=None),
    phone_number: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Если прислали JSON — используем его.
    if payload is None:
        # Если JSON не пришёл, собираем из формы (name обязателен)
        if not name:
            raise HTTPException(status_code=422, detail="name is required")
        payload = WorkerCreate(name=name, phone_number=phone_number)

    worker = crud_worker.create_worker(
        db,
        name=payload.name.strip(),
        phone_number=(payload.phone_number or "").strip() or None,
        user_id=current_user.id,
    )
    return worker
