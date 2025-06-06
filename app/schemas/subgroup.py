from pydantic import BaseModel
from typing import Optional


class SubgroupBase(BaseModel):
    name: str


class SubgroupCreate(SubgroupBase):
    pass


class Subgroup(SubgroupBase):
    id: int

    class Config:
        from_attributes = True

class SubgroupUpdate(BaseModel):
    name: str
