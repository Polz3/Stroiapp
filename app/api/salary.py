from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user

from app.database.db import get_db
from app.schemas.salary import Salary, SalaryCreate, SalaryUpdate
import app.crud.salary as crud

router = APIRouter(
    prefix="/api/sites",
    tags=["sites"],
    dependencies=[Depends(get_current_user)]  # ← вот это обязательно
)

@router.get("/", response_model=list[Salary])
def read_salaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_salaries(db, skip, limit)

@router.post("/", response_model=Salary)
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db)):
    return crud.create_salary(db, salary)

@router.get("/{salary_id}", response_model=Salary)
def read_salary(salary_id: int, db: Session = Depends(get_db)):
    db_sal = crud.get_salary(db, salary_id)
    if not db_sal:
        raise HTTPException(404, "Salary not found")
    return db_sal

@router.put("/{salary_id}", response_model=Salary)
def update_salary(salary_id: int, salary: SalaryUpdate, db: Session = Depends(get_db)):
    updated = crud.update_salary(db, salary_id, salary)
    if not updated:
        raise HTTPException(404, "Salary not found")
    return updated

@router.delete("/{salary_id}")
def delete_salary(salary_id: int, db: Session = Depends(get_db)):
    success = crud.delete_salary(db, salary_id)
    if not success:
        raise HTTPException(404, "Salary not found")
    return {"message": "Salary deleted successfully"}
