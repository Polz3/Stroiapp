from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database.db import get_db  # Убедись, что путь правильный

router = APIRouter(prefix="/api/purchases", tags=["Purchases"])


@router.post("/", response_model=schemas.Expense)
def create_purchase(purchase: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    if purchase.type != "purchase":
        raise HTTPException(status_code=400, detail="Тип расхода должен быть 'purchase'")
    return crud.expense.create(db, purchase)


@router.get("/", response_model=List[schemas.Expense])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.expense.get_by_type(db, type="purchase", skip=skip, limit=limit)
