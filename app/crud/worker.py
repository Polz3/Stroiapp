from sqlalchemy.orm import Session
from app.models.worker import Worker
from app.schemas.worker import WorkerCreate, WorkerUpdate

def create_worker(db: Session, worker: WorkerCreate) -> Worker:
    db_worker = Worker(**worker.model_dump(), is_archived=False)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def get_workers(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    include_archived: bool = False
) -> list[Worker]:
    query = db.query(Worker).filter(Worker.user_id == user_id)
    if not include_archived:
        query = query.filter(Worker.is_archived == False)
    return query.offset(skip).limit(limit).all()

def get_worker(db: Session, worker_id: int) -> Worker | None:
    return db.query(Worker).filter(Worker.id == worker_id).first()

def update_worker(db: Session, worker_id: int, worker_update: WorkerUpdate) -> Worker | None:
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return None
    data = worker_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_worker, field, value)
    db.commit()
    db.refresh(db_worker)
    return db_worker

def archive_worker(db: Session, worker_id: int) -> Worker | None:
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return None
    db_worker.is_archived = True
    db.commit()
    db.refresh(db_worker)
    return db_worker

def restore_worker(db: Session, worker_id: int) -> Worker | None:
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return None
    db_worker.is_archived = False
    db.commit()
    db.refresh(db_worker)
    return db_worker

def delete_worker(db: Session, worker_id: int) -> bool:
    db_worker = get_worker(db, worker_id)
    if not db_worker:
        return False
    db.delete(db_worker)
    db.commit()
    return True
