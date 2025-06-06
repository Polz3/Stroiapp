from pydantic import BaseModel
from typing import Optional
from datetime import date
from datetime import datetime

# Схема для создания расхода
class ExpenseCreate(BaseModel):
    amount: float
    type: str  # 'purchase' или 'salary'
    site_id: Optional[int] = None
    worker_id: Optional[int] = None
    comment: Optional[str] = None
    date: datetime



# Схема для обновления расхода
class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    site_id: Optional[int] = None
    worker_id: Optional[int] = None
    comment: Optional[str] = None
    date: Optional[date] = None


# Схема для отображения расхода
class Expense(BaseModel):
    id: int
    amount: float
    type: str
    site_id: Optional[int] = None
    worker_id: Optional[int] = None
    comment: Optional[str] = None
    date: date

    class Config:
        from_attributes = True
