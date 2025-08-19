# app/api/salary.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
import app.crud.salary as crud_sal
from app.api.auth import get_current_user
from app.models.models import User
from app.schemas.salary import Salary as SalaryOut, SalaryCreate, SalaryUpdate

router = APIRouter(prefix="/api/salaries", tags=["salaries"])

# Список зарплат (текущего пользователя)
@router.get("", response_model=List[SalaryOut])
@router.get("/", response_model=List[SalaryOut])
def list_salaries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_sal.get_salaries(db, user_id=current_user.id)

# Одна зарплата
@router.get("/{salary_id}", response_model=SalaryOut)
def read_salary(
    salary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sal = crud_sal.get_salary(db, salary_id, user_id=current_user.id)
    if not sal:
        raise HTTPException(status_code=404, detail="Salary not found")
    return sal

# Создать зарплату
@router.post("", response_model=SalaryOut)
@router.post("/", response_model=SalaryOut)
def create_salary(
    payload: SalaryCreate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # SalaryCreate уже содержит: amount, date, comment?, site_id?, worker_id
    return crud_sal.create_salary(db, payload, user_id=current_user.id)

# Обновить зарплату
@router.put("/{salary_id}", response_model=SalaryOut)
def update_salary(
    salary_id: int,
    payload: SalaryUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sal = crud_sal.update_salary(db, salary_id, payload, user_id=current_user.id)
    if not sal:
        raise HTTPException(status_code=404, detail="Salary not found")
    return sal

# Удалить зарплату
@router.delete("/{salary_id}")
def delete_salary(
    salary_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = crud_sal.delete_salary(db, salary_id, user_id=current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Salary not found")
    return {"ok": True}
