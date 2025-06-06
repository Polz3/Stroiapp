from pydantic import BaseModel
from typing import Optional
from datetime import date


# Схема для создания инструмента
class ToolCreate(BaseModel):
    name: str
    quantity: int
    comment: Optional[str] = None


# Схема для обновления инструмента
class ToolUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    comment: Optional[str] = None


# Схема для отображения инструмента
class Tool(BaseModel):
    id: int
    name: str
    quantity: int
    comment: Optional[str] = None
    site_id: Optional[int] = None  # Если инструмент уже прикреплен к объекту

    class Config:
        from_attributes = True


# Схема для создания перемещения инструмента
class ToolTransferCreate(BaseModel):
    tool_id: int
    from_site_id: Optional[int] = None  # None = склад
    to_site_id: Optional[int] = None    # None = склад
    comment: Optional[str] = None
    date: date


# Схема для отображения перемещения инструмента
class ToolTransfer(BaseModel):
    id: int
    tool_id: int
    from_site_id: Optional[int] = None
    to_site_id: Optional[int] = None
    comment: Optional[str] = None
    date: date

    class Config:
        from_attributes = True
