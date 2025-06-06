from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import date as date_type


def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Expense]:
    return (
        db.query(Expense)
          .filter(Expense.user_id == user_id)
          .order_by(Expense.date.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )

def get_expense(db: Session, expense_id: int) -> Expense | None:
    return db.query(Expense).filter(Expense.id == expense_id).first()

def create_expense(db: Session, amount: float, site_id: int | None, comment: str, date: date_type, user_id: int):
    db_exp = Expense(
        amount=amount,
        site_id=site_id,
        comment=comment,
        date=date,
        type="purchase",
        user_id=user_id
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def update_expense(db: Session, expense_id: int, expense_update: ExpenseUpdate) -> Expense | None:
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return None
    data = expense_update.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_expense, field, value)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int) -> bool:
    db_expense = get_expense(db, expense_id)
    if not db_expense:
        return False
    db.delete(db_expense)
    db.commit()
    return True

def get_expenses_by_type(db: Session, user_id: int, type: str, skip: int = 0, limit: int = 100) -> list[Expense]:
    return (
        db.query(Expense)
          .filter(Expense.type == type, Expense.user_id == user_id)
          .order_by(Expense.date.desc())
          .offset(skip)
          .limit(limit)
          .all()
    )
