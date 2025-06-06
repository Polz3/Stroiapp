from pydantic import BaseModel
from typing import Optional
from datetime import date

class SalaryBase(BaseModel):
    amount: float
    date: date
    comment: Optional[str] = None
    site_id: Optional[int] = None
    worker_id: int

    class Config:
        from_attributes = True

class SalaryCreate(SalaryBase):
    pass

class SalaryUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[date] = None
    comment: Optional[str] = None
    site_id: Optional[int] = None
    worker_id: Optional[int] = None

    class Config:
        orm_mode = True

class Salary(SalaryBase):
    id: int
