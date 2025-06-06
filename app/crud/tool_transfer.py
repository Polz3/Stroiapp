from sqlalchemy.orm import Session
from app.models.models import ToolTransfer
from app.schemas.tool_transfer import ToolTransferCreate, ToolTransferUpdate

def get_tool_transfers(db: Session, skip: int = 0, limit: int = 100) -> list[ToolTransfer]:
    return db.query(ToolTransfer).offset(skip).limit(limit).all()

def get_tool_transfer(db: Session, transfer_id: int) -> ToolTransfer | None:
    return db.query(ToolTransfer).filter(ToolTransfer.id == transfer_id).first()

def create_tool_transfer(db: Session, transfer: ToolTransferCreate) -> ToolTransfer:
    db_tr = ToolTransfer(**transfer.model_dump())
    db.add(db_tr)
    db.commit()
    db.refresh(db_tr)
    return db_tr

def update_tool_transfer(db: Session, transfer_id: int, tr_update: ToolTransferUpdate) -> ToolTransfer | None:
    db_tr = get_tool_transfer(db, transfer_id)
    if not db_tr:
        return None
    data = tr_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_tr, f, v)
    db.commit()
    db.refresh(db_tr)
    return db_tr

def delete_tool_transfer(db: Session, transfer_id: int) -> bool:
    db_tr = get_tool_transfer(db, transfer_id)
    if not db_tr:
        return False
    db.delete(db_tr)
    db.commit()
    return True

def get_all(db: Session):
    return db.query(ToolTransfer).order_by(ToolTransfer.date_value.desc()).all()