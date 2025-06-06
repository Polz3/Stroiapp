from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.salary import Salary, SalaryCreate, SalaryUpdate
from app.crud import salary as crud_salary
from app.database.deps import get_db

router = APIRouter(prefix="/api/salaries", tags=["Salaries"])

# Получить все записи о зарплатах
@router.get("/", response_model=List[Salary])
def read_salaries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_salary.get_salaries(db, user_id=current_user.id, skip=skip, limit=limit)

# Получить конкретную запись о зарплате
@router.get("/{salary_id}", response_model=Salary)
def read_salary(salary_id: int, db: Session = Depends(get_db)):
    db_salary = crud_salary.get_salary(db, salary_id)
    if db_salary is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    return db_salary

# Создать новую запись о зарплате
@router.post("/", response_model=Salary)
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_salary.create_salary(db, salary, user_id=current_user.id)

# Обновить запись о зарплате
@router.put("/{salary_id}", response_model=Salary)
def update_salary(salary_id: int, salary: SalaryUpdate, db: Session = Depends(get_db)):
    db_salary = crud_salary.update_salary(db, salary_id, salary)
    if db_salary is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    return db_salary

# Удалить запись о зарплате
@router.delete("/{salary_id}")
def delete_salary(salary_id: int, db: Session = Depends(get_db)):
    success = crud_salary.delete_salary(db, salary_id)
    if not success:
        raise HTTPException(status_code=404, detail="Salary not found")
    return {"ok": True}
