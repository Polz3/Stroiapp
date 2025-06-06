# app/schemas/tool_transfer.py

from datetime import datetime
from pydantic import BaseModel

class ToolTransferBase(BaseModel):
    tool_id: int
    from_site_id: int
    to_site_id: int
    comment: str | None = None
    date_value: datetime | None = None

class ToolTransferCreate(ToolTransferBase):
    pass

class ToolTransferUpdate(BaseModel):
    comment: str | None = None
    date_value: datetime | None = None

class ToolTransfer(ToolTransferBase):
    id: int

    class Config:
        orm_mode = True
