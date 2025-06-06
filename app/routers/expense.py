from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app import crud, models, schemas
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Создание нового расхода
@router.post("/", response_model=models.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.expense.create(db, expense, user_id=current_user.id)


# Получение всех расходов
@router.get("/", response_model=list[models.Expense])
def read_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 100):
    return crud.expense.get_all(db, user_id=current_user.id, skip=skip, limit=limit)

# Получение одного расхода по ID
@router.get("/{expense_id}", response_model=models.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = crud.expense.get(db, expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

# Обновление расхода по ID
@router.put("/{expense_id}", response_model=models.Expense)
def update_expense(expense_id: int, updated: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.expense.update(db, expense_id, updated)

# Удаление расхода по ID
@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    crud.expense.delete(db, expense_id)
    return {"message": "Expense deleted"}
