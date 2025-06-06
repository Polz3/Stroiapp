from pydantic import BaseModel
from typing import Optional

class WorkerBase(BaseModel):
    name: str
    phone: Optional[str] = None

class WorkerCreate(WorkerBase):
    pass

class WorkerUpdate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int

    class Config:
        from_attributes = True
