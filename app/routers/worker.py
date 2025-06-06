# app/routers/worker.py

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from app.database.db import get_db
from app import crud
from app.schemas import worker as schemas
from app.schemas.worker import Worker  # ✅ Pydantic-модель
from app.crud import salary as crud_salary, site as crud_site

router = APIRouter(prefix="/workers", tags=["Workers"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/", response_model=Worker)
def create_worker(worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.worker.create(db, worker)


@router.get("/", response_model=list[Worker])
def read_workers(db: Session = Depends(get_db)):
    return crud.worker.get_all(db)


@router.get("/{worker_id}", response_model=Worker)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    db_worker = crud.worker.get(db, worker_id)
    if db_worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker


@router.put("/{worker_id}", response_model=Worker)
def update_worker(worker_id: int, updated: schemas.WorkerCreate, db: Session = Depends(get_db)):
    return crud.worker.update(db, worker_id, updated)


@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    crud.worker.delete(db, worker_id)
    return {"message": "Worker deleted"}


@router.get("/{worker_id}/card")
def worker_detail(worker_id: int, request: Request, db: Session = Depends(get_db)):
    worker = crud.worker.get_worker(db, worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")

    salaries = crud_salary.get_salaries_by_worker(db, worker_id)
    all_sites = crud_site.get_sites_by_worker(db, worker_id)
    active_sites = [s for s in all_sites if not s.is_archived]
    archived_sites = [s for s in all_sites if s.is_archived]

    return templates.TemplateResponse("worker_detail.html", {
        "request": request,
        "worker": worker,
        "salaries": salaries,
        "active_sites": active_sites,
        "archived_sites": archived_sites,
    })
