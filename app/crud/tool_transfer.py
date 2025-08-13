from sqlalchemy.orm import Session
from app.models.models import ToolTransfer
from app.schemas.tool_transfer import ToolTransferCreate, ToolTransferUpdate

def get_tool_transfers(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> list[ToolTransfer]:
    return (
        db.query(ToolTransfer)
        .filter(ToolTransfer.user_id == user_id)
        .order_by(ToolTransfer.date_value.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_tool_transfer(db: Session, transfer_id: int, user_id: int) -> ToolTransfer | None:
    return (
        db.query(ToolTransfer)
        .filter(ToolTransfer.id == transfer_id, ToolTransfer.user_id == user_id)
        .first()
    )

def create_tool_transfer(db: Session, transfer: ToolTransferCreate, user_id: int) -> ToolTransfer:
    db_tr = ToolTransfer(**transfer.model_dump(), user_id=user_id)
    db.add(db_tr)
    db.commit()
    db.refresh(db_tr)
    return db_tr

def update_tool_transfer(
    db: Session,
    transfer_id: int,
    tr_update: ToolTransferUpdate,
    user_id: int
) -> ToolTransfer | None:
    db_tr = get_tool_transfer(db, transfer_id, user_id)
    if not db_tr:
        return None
    data = tr_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_tr, f, v)
    db.commit()
    db.refresh(db_tr)
    return db_tr

def delete_tool_transfer(db: Session, transfer_id: int, user_id: int) -> bool:
    db_tr = get_tool_transfer(db, transfer_id, user_id)
    if not db_tr:
        return False
    db.delete(db_tr)
    db.commit()
    return True

def get_all(db: Session, user_id: int) -> list[ToolTransfer]:
    return (
        db.query(ToolTransfer)
        .filter(ToolTransfer.user_id == user_id)
        .order_by(ToolTransfer.date_value.desc())
        .all()
    )
