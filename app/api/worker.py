from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.worker import Worker, WorkerCreate, WorkerUpdate
import app.crud.worker as crud_worker

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("/", response_model=Worker)
def create_worker_endpoint(worker: WorkerCreate, db: Session = Depends(get_db)):
    return crud_worker.create_worker(db, worker)

@router.get("/", response_model=list[Worker])
def read_workers(skip: int = 0, limit: int = 100, archived: bool = False, db: Session = Depends(get_db)):
    return crud_worker.get_workers(db, skip, limit, include_archived=archived)

@router.get("/{worker_id}", response_model=Worker)
def read_worker(worker_id: int, db: Session = Depends(get_db)):
    db_worker = crud_worker.get_worker(db, worker_id)
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_worker

@router.put("/{worker_id}", response_model=Worker)
def update_worker_endpoint(worker_id: int, worker: WorkerUpdate, db: Session = Depends(get_db)):
    updated = crud_worker.update_worker(db, worker_id, worker)
    if not updated:
        raise HTTPException(status_code=404, detail="Worker not found")
    return updated

@router.post("/{worker_id}/archive", response_model=Worker)
def archive_worker_endpoint(worker_id: int, db: Session = Depends(get_db)):
    archived = crud_worker.archive_worker(db, worker_id)
    if not archived:
        raise HTTPException(status_code=404, detail="Worker not found")
    return archived

@router.post("/{worker_id}/restore", response_model=Worker)
def restore_worker_endpoint(worker_id: int, db: Session = Depends(get_db)):
    restored = crud_worker.restore_worker(db, worker_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Worker not found")
    return restored

@router.delete("/{worker_id}")
def delete_worker_endpoint(worker_id: int, db: Session = Depends(get_db)):
    success = crud_worker.delete_worker(db, worker_id)
    if not success:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"message": "Worker deleted successfully"}
