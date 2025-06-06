# app/routers/material.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app import crud, models

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.post("/", response_model=models.Material)
def create_material(material: models.MaterialCreate, db: Session = Depends(get_db)):
    return crud.material.create(db, material)


@router.get("/", response_model=list[models.Material])
def read_materials(db: Session = Depends(get_db)):
    return crud.material.get_all(db)


@router.get("/{material_id}", response_model=models.Material)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = crud.material.get(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material


@router.put("/{material_id}", response_model=models.Material)
def update_material(material_id: int, updated: models.MaterialCreate, db: Session = Depends(get_db)):
    return crud.material.update(db, material_id, updated)


@router.delete("/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    crud.material.delete(db, material_id)
    return {"message": "Material deleted"}
