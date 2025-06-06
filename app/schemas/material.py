from pydantic import BaseModel
from typing import Optional


class MaterialBase(BaseModel):
    name: str
    unit: Optional[str] = None
    is_archived: bool = False


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(MaterialBase):
    name: Optional[str] = None
    unit: Optional[str] = None
    is_archived: Optional[bool] = None


class Material(MaterialBase):
    id: int

    class Config:
        from_attributes = True  # для Pydantic V2
