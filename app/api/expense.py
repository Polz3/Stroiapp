from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.auth import get_current_user

from app.database.db import get_db
from app.schemas.expense import Expense, ExpenseCreate, ExpenseUpdate
import app.crud.expense as crud

router = APIRouter(
    prefix="/api/salaries",
    tags=["salaries"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=list[Expense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_expenses(db, skip=skip, limit=limit)

@router.post("/", response_model=Expense)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)

@router.get("/{expense_id}", response_model=Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_exp = crud.get_expense(db, expense_id)
    if not db_exp:
        raise HTTPException(404, "Expense not found")
    return db_exp

@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    updated = crud.update_expense(db, expense_id, expense)
    if not updated:
        raise HTTPException(404, "Expense not found")
    return updated

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    success = crud.delete_expense(db, expense_id)
    if not success:
        raise HTTPException(404, "Expense not found")
    return {"message": "Expense deleted successfully"}
