# app/crud/subgroups.py
from sqlalchemy.orm import Session
from app.models.models import Subgroup
from app.schemas.subgroup import SubgroupCreate, SubgroupUpdate
from typing import Optional

def get_subgroups(db: Session, user_id: Optional[int] = None) -> list[Subgroup]:
    query = db.query(Subgroup)
    if user_id is not None:
        query = query.filter(Subgroup.user_id == user_id)
    return query.order_by(Subgroup.id.desc()).all()

def create_subgroup(db: Session, subgroup: SubgroupCreate, user_id: int):
    db_subgroup = Subgroup(name=subgroup.name, user_id=user_id)
    db.add(db_subgroup)
    db.commit()
    db.refresh(db_subgroup)
    return db_subgroup

def get_subgroup_by_id(db: Session, subgroup_id: int, user_id: Optional[int] = None) -> Subgroup | None:
    query = db.query(Subgroup).filter(Subgroup.id == subgroup_id)
    if user_id is not None:
        query = query.filter(Subgroup.user_id == user_id)
    return query.first()

def update_subgroup(db: Session, subgroup_id: int, name: str, user_id: Optional[int] = None) -> Subgroup | None:
    query = db.query(Subgroup).filter(Subgroup.id == subgroup_id)
    if user_id is not None:
        query = query.filter(Subgroup.user_id == user_id)
    db_subgroup = query.first()
    if db_subgroup:
        db_subgroup.name = name
        db.commit()
        db.refresh(db_subgroup)
    return db_subgroup

def delete_subgroup(db: Session, subgroup_id: int, user_id: Optional[int] = None) -> Subgroup | None:
    query = db.query(Subgroup).filter(Subgroup.id == subgroup_id)
    if user_id is not None:
        query = query.filter(Subgroup.user_id == user_id)
    db_subgroup = query.first()
    if db_subgroup:
        db.delete(db_subgroup)
        db.commit()
    return db_subgroup
