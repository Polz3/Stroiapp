from pydantic import BaseModel
from typing import Optional


class SiteBase(BaseModel):
    name: str
    address: Optional[str] = None
    subgroup_id: Optional[int] = None


class SiteCreate(SiteBase):
    pass


class SiteUpdate(SiteBase):
    is_archived: Optional[bool] = None


class Site(SiteBase):
    id: int
    is_archived: bool

    class Config:
        from_attributes = True  # Используем from_attributes для совместимости с Pydantic V2
