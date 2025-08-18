# app/api/worker.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
import app.crud.worker as crud_worker
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(prefix="/api/workers", tags=["Workers"])

@router.get("/")
def read_workers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_worker.get_workers(db, user_id=current_user.id)

@router.get("/{worker_id}")
def read_worker(
    worker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    w = crud_worker.get_worker(db, worker_id)
    if not w or w.user_id != current_user.id:
        raise HTTPException(404, "Worker not found")
    return w
