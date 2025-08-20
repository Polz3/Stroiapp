from pydantic import BaseModel
from datetime import date
from typing import Optional
from .tool_transfer import ToolTransfer, ToolTransferCreate, ToolTransferUpdate

# Схема для объекта Site
class SiteBase(BaseModel):
    name: str
    address: Optional[str] = None
    archived: bool = False
    subgroup_id: Optional[int] = None

class SiteCreate(SiteBase):
    pass

class SiteUpdate(SiteBase):
    pass

class Site(SiteBase):
    id: int

    class Config:
        orm_mode = True

# Схема для подгруппы
class SubgroupBase(BaseModel):
    name: str

class SubgroupCreate(SubgroupBase):
    pass

class Subgroup(SubgroupBase):
    id: int

    class Config:
        orm_mode = True

# Схема для инструмента
class ToolBase(BaseModel):
    name: str
    current_location: str
    is_archived: bool = False

class ToolCreate(ToolBase):
    pass

class ToolUpdate(ToolBase):
    pass

class Tool(ToolBase):
    id: int

    class Config:
        orm_mode = True

# Схема для работника
class WorkerBase(BaseModel):
    name: str
    phone_number: Optional[str] = None

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int

    class Config:
        orm_mode = True

# Схема для материала
class MaterialBase(BaseModel):
    name: str
    quantity: int
    unit: str

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int

    class Config:
        orm_mode = True

# Схема для расхода
class ExpenseBase(BaseModel):
    amount: float
    comment: Optional[str] = None
    date: date
    site_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int

    class Config:
        orm_mode = True

# Схема для закупки
class PurchaseBase(BaseModel):
    amount: float  # Сумма закупки
    comment: str   # Комментарий
    site_id: int   # ID объекта
    date: date     # Дата операции

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int

    class Config:
        orm_mode = True

# Схема для зарплаты
class SalaryBase(BaseModel):
    amount: float
    comment: Optional[str] = None
    date: date
    worker_id: int

class SalaryCreate(SalaryBase):
    pass

class SalaryUpdate(SalaryBase):
    pass

class Salary(SalaryBase):
    id: int

    class Config:
        orm_mode = True
