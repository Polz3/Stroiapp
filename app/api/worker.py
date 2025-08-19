# app/api/worker.py
from fastapi import APIRouter, Depends, HTTPException, Body
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
    w = crud_worker.get_worker(db, worker_id, current_user.id)
    if not w:
        raise HTTPException(status_code=404, detail="Worker not found")
    return w


# --- Создать сотрудника ---
@router.post("", response_model=WorkerOut)
@router.post("/", response_model=WorkerOut)
def create_worker(
    payload: WorkerCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # привести к аккуратному виду
    payload = WorkerCreate(
        name=payload.name.strip(),
        phone_number=(payload.phone_number or "").strip() or None,
    )
    worker = crud_worker.create_worker(db, payload, user_id=current_user.id)
    return worker
