from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.material import Material, MaterialCreate, MaterialUpdate
import app.crud.material as crud

router = APIRouter(prefix="/materials", tags=["Materials"])

@router.get("/", response_model=list[Material])
def read_materials(skip: int = 0, limit: int = 100, archived: bool = False, db: Session = Depends(get_db)):
    return crud.get_materials(db, skip, limit, include_archived=archived)

@router.get("/{material_id}", response_model=Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_mat = crud.get_material(db, material_id)
    if not db_mat:
        raise HTTPException(404, "Material not found")
    return db_mat

@router.post("/", response_model=Material)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    return crud.create_material(db, material)

@router.put("/{material_id}", response_model=Material)
def update_material(material_id: int, material: MaterialUpdate, db: Session = Depends(get_db)):
    updated = crud.update_material(db, material_id, material)
    if not updated:
        raise HTTPException(404, "Material not found")
    return updated

@router.post("/{material_id}/archive", response_model=Material)
def archive_material(material_id: int, db: Session = Depends(get_db)):
    archived = crud.archive_material(db, material_id)
    if not archived:
        raise HTTPException(404, "Material not found")
    return archived

@router.post("/{material_id}/restore", response_model=Material)
def restore_material(material_id: int, db: Session = Depends(get_db)):
    restored = crud.restore_material(db, material_id)
    if not restored:
        raise HTTPException(404, "Material not found")
    return restored

@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    success = crud.delete_material(db, material_id)
    if not success:
        raise HTTPException(404, "Material not found")
    return {"message": "Material deleted successfully"}
