from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.tool import Tool, ToolCreate, ToolUpdate
import app.crud.tool as crud

router = APIRouter(prefix="/tools", tags=["Tools"])

@router.get("/", response_model=list[Tool])
def read_tools(skip: int = 0, limit: int = 100, archived: bool = False, db: Session = Depends(get_db)):
    return crud.get_tools(db, skip, limit, include_archived=archived)

@router.get("/{tool_id}", response_model=Tool)
def read_tool(tool_id: int, db: Session = Depends(get_db)):
    db_tool = crud.get_tool(db, tool_id)
    if not db_tool:
        raise HTTPException(404, "Tool not found")
    return db_tool

@router.post("/", response_model=Tool)
def create_tool(tool: ToolCreate, db: Session = Depends(get_db)):
    return crud.create_tool(db, tool)

@router.put("/{tool_id}", response_model=Tool)
def update_tool(tool_id: int, tool: ToolUpdate, db: Session = Depends(get_db)):
    updated = crud.update_tool(db, tool_id, tool)
    if not updated:
        raise HTTPException(404, "Tool not found")
    return updated

@router.post("/{tool_id}/archive", response_model=Tool)
def archive_tool(tool_id: int, db: Session = Depends(get_db)):
    archived = crud.archive_tool(db, tool_id)
    if not archived:
        raise HTTPException(404, "Tool not found")
    return archived

@router.post("/{tool_id}/restore", response_model=Tool)
def restore_tool(tool_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_tool(db, tool_id)
    if not restored:
        raise HTTPException(404, "Tool not found")
    return restored

@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    success = crud.delete_tool(db, tool_id)
    if not success:
        raise HTTPException(404, "Tool not found")
    return {"message": "Tool deleted successfully"}
