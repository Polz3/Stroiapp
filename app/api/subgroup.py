from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.schemas.subgroup import Subgroup, SubgroupCreate, SubgroupUpdate
import app.crud.subgroups as crud

router = APIRouter(prefix="/subgroups", tags=["Subgroups"])

@router.get("/", response_model=list[Subgroup])
def read_subgroups(db: Session = Depends(get_db)):
    return crud.get_subgroups(db)

@router.post("/", response_model=Subgroup)
def create_subgroup(subgroup: SubgroupCreate, db: Session = Depends(get_db)):
    return crud.create_subgroup(db, subgroup)

@router.get("/{subgroup_id}", response_model=Subgroup)
def read_subgroup(subgroup_id: int, db: Session = Depends(get_db)):
    db_sg = crud.get_subgroup(db, subgroup_id)
    if not db_sg:
        raise HTTPException(404, "Subgroup not found")
    return db_sg

@router.put("/{subgroup_id}", response_model=Subgroup)
def update_subgroup(subgroup_id: int, subgroup: SubgroupUpdate, db: Session = Depends(get_db)):
    updated = crud.update_subgroup(db, subgroup_id, subgroup)
    if not updated:
        raise HTTPException(404, "Subgroup not found")
    return updated

@router.delete("/{subgroup_id}")
def delete_subgroup(subgroup_id: int, db: Session = Depends(get_db)):
    success = crud.delete_subgroup(db, subgroup_id)
    if not success:
        raise HTTPException(404, "Subgroup not found")
    return {"message": "Subgroup deleted successfully"}
