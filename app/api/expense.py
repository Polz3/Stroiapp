from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.db import get_db
from app.api.auth import get_current_user
from app.models.models import User

from app.schemas.expense import Expense, ExpenseCreate, ExpenseUpdate
import app.crud.expense as crud

router = APIRouter(
    prefix="/api/expenses",          # корректный префикс
    tags=["expenses"],
    dependencies=[Depends(get_current_user)],
    redirect_slashes=False           # чтобы не было 307 между / и без /
)

# --- Список расходов (поддержка и "" и "/") ---
@router.get("", response_model=List[Expense])
@router.get("/", response_model=List[Expense])
def read_expenses(
    site_id: Optional[int] = None,
    type: Optional[str] = None,      # "purchase" | "salary" | None
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Базовая выборка по user_id
    items = crud.get_expenses(db, user_id=current_user.id, skip=skip, limit=limit)

    # Дополнительные фильтры (если нужны с фронта)
    if site_id is not None:
        items = [e for e in items if e.site_id == site_id]
    if type is not None:
        items = [e for e in items if e.type == type]
    return items

# --- Создание расхода ---
@router.post("/", response_model=Expense)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Твой CRUD ожидает поля по отдельности, не объект схемы:
    # create_expense(db, amount: float, site_id: int|None, comment: str, date: date, user_id: int)
    return crud.create_expense(
        db,
        amount=payload.amount,
        site_id=payload.site_id,
        comment=payload.comment,
        date=payload.date,
        user_id=current_user.id,
    )

# --- Получение одного расхода ---
@router.get("/{expense_id}", response_model=Expense)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_exp = crud.get_expense(db, expense_id, user_id=current_user.id)
    if not db_exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_exp

# --- Обновление ---
@router.put("/{expense_id}", response_model=Expense)
def update_expense(
    expense_id: int,
    payload: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = crud.update_expense(db, expense_id, payload, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated

# --- Удаление ---
@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = crud.delete_expense(db, expense_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}
