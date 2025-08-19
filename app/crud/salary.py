from sqlalchemy.orm import Session
from app.models.salary import Salary
from app.schemas.salary import SalaryCreate, SalaryUpdate
from typing import Optional

def get_salaries(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Salary]:
    return (
        db.query(Salary)
        .filter(Salary.user_id == user_id)
        .order_by(Salary.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_salary(db: Session, salary_id: int, user_id: int) -> Salary | None:
    return (
        db.query(Salary)
        .filter(Salary.id == salary_id, Salary.user_id == user_id)
        .first()
    )

def create_salary(db: Session, salary: SalaryCreate, user_id: int, site_id: Optional[int] = None) -> Salary:
    db_sal = Salary(**salary.model_dump(), user_id=user_id, site_id=site_id)
    db.add(db_sal)
    db.commit()
    db.refresh(db_sal)
    return db_sal

def update_salary(db: Session, salary_id: int, sal_update: SalaryUpdate, user_id: int) -> Salary | None:
    db_sal = get_salary(db, salary_id, user_id=user_id)
    if not db_sal:
        return None
    data = sal_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_sal, f, v)
    db.commit()
    db.refresh(db_sal)
    return db_sal

def delete_salary(db: Session, salary_id: int, user_id: int) -> bool:
    db_sal = get_salary(db, salary_id, user_id=user_id)
    if not db_sal:
        return False
    db.delete(db_sal)
    db.commit()
    return True

def get_salaries_by_worker(db: Session, worker_id: int, user_id: int) -> list[Salary]:
    return (
        db.query(Salary)
        .filter(Salary.worker_id == worker_id, Salary.user_id == user_id)
        .order_by(Salary.date.desc())
        .all()
    )
