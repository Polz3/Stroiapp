from sqlalchemy.orm import Session
from app.models.salary import Salary
from app.schemas.salary import SalaryCreate, SalaryUpdate

def get_salaries(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Salary]:
    return (
        db.query(Salary)
        .filter(Salary.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_salary(db: Session, salary_id: int) -> Salary | None:
    return db.query(Salary).filter(Salary.id == salary_id).first()

def create_salary(db: Session, salary: SalaryCreate, user_id: int) -> Salary:
    db_sal = Salary(**salary.model_dump(), user_id=user_id)
    db.add(db_sal)
    db.commit()
    db.refresh(db_sal)
    print("💾 Зарплата сохранена:", db_sal.amount, db_sal.worker_id, db_sal.date)  # ← временно
    return db_sal

def update_salary(db: Session, salary_id: int, sal_update: SalaryUpdate) -> Salary | None:
    db_sal = get_salary(db, salary_id)
    if not db_sal:
        return None
    data = sal_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_sal, f, v)
    db.commit()
    db.refresh(db_sal)
    return db_sal

def delete_salary(db: Session, salary_id: int) -> bool:
    db_sal = get_salary(db, salary_id)
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

def get_salaries_by_worker(db: Session, worker_id: int) -> list[Salary]:
    print("📌 get_salaries_by_worker вызван для worker_id:", worker_id)
    return (
        db.query(Salary)
        .filter(Salary.worker_id == worker_id)
        .order_by(Salary.date.desc())
        .all()
    )

