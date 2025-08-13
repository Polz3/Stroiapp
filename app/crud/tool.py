from sqlalchemy.orm import Session
from app.models.tool import Tool
from app.schemas.tool import ToolCreate, ToolUpdate

def get_tools(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    include_archived: bool = False
) -> list[Tool]:
    q = db.query(Tool).filter(Tool.user_id == user_id)
    if not include_archived:
        q = q.filter(Tool.is_archived == False)
    return q.offset(skip).limit(limit).all()

def get_tool(db: Session, tool_id: int, user_id: int) -> Tool | None:
    return (
        db.query(Tool)
        .filter(Tool.id == tool_id, Tool.user_id == user_id)
        .first()
    )

def create_tool(db: Session, tool: ToolCreate, user_id: int) -> Tool:
    db_tool = Tool(**tool.model_dump(), user_id=user_id, is_archived=False)
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def update_tool(db: Session, tool_id: int, tool_update: ToolUpdate, user_id: int) -> Tool | None:
    db_tool = get_tool(db, tool_id, user_id)
    if not db_tool:
        return None
    data = tool_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_tool, f, v)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def archive_tool(db: Session, tool_id: int, user_id: int) -> Tool | None:
    db_tool = get_tool(db, tool_id, user_id)
    if not db_tool:
        return None
    db_tool.is_archived = True
    db.commit()
    db.refresh(db_tool)
    return db_tool

def restore_tool(db: Session, tool_id: int, user_id: int) -> Tool | None:
    db_tool = get_tool(db, tool_id, user_id)
    if not db_tool:
        return None
    db_tool.is_archived = False
    db.commit()
    db.refresh(db_tool)
    return db_tool

def delete_tool(db: Session, tool_id: int, user_id: int) -> bool:
    db_tool = get_tool(db, tool_id, user_id)
    if not db_tool:
        return False
    db.delete(db_tool)
    db.commit()
    return True

def get_all(db: Session, user_id: int) -> list[Tool]:
    return db.query(Tool).filter(Tool.user_id == user_id).all()
