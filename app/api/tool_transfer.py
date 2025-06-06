from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.schemas import ToolTransfer, ToolTransferCreate, ToolTransferUpdate
import app.crud.tool_transfer as crud

router = APIRouter(prefix="/tool-transfers", tags=["Tool Transfers"])

@router.get("/", response_model=list[ToolTransfer])
def read_transfers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tool_transfers(db, skip, limit)

@router.post("/", response_model=ToolTransfer)
def create_transfer(transfer: ToolTransferCreate, db: Session = Depends(get_db)):
    return crud.create_tool_transfer(db, transfer)

@router.get("/{transfer_id}", response_model=ToolTransfer)
def read_transfer(transfer_id: int, db: Session = Depends(get_db)):
    db_tr = crud.get_tool_transfer(db, transfer_id)
    if not db_tr:
        raise HTTPException(404, "ToolTransfer not found")
    return db_tr

@router.put("/{transfer_id}", response_model=ToolTransfer)
def update_transfer(transfer_id: int, transfer: ToolTransferUpdate, db: Session = Depends(get_db)):
    updated = crud.update_tool_transfer(db, transfer_id, transfer)
    if not updated:
        raise HTTPException(404, "ToolTransfer not found")
    return updated

@router.delete("/{transfer_id}")
def delete_transfer(transfer_id: int, db: Session = Depends(get_db)):
    success = crud.delete_tool_transfer(db, transfer_id)
    if not success:
        raise HTTPException(404, "ToolTransfer not found")
    return {"message": "ToolTransfer deleted successfully"}
