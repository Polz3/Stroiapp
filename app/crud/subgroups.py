from sqlalchemy.orm import Session
from app.models.models import Subgroup
from app.schemas.subgroup import SubgroupCreate, SubgroupUpdate

def get_subgroups(db: Session) -> list[Subgroup]:
    return db.query(Subgroup).all()

def create_subgroup(db: Session, subgroup: SubgroupCreate):
    db_subgroup = Subgroup(name=subgroup.name)
    db.add(db_subgroup)
    db.commit()
    db.refresh(db_subgroup)
    return db_subgroup

def get_subgroup_by_id(db: Session, subgroup_id: int) -> Subgroup | None:
    return db.query(Subgroup).filter(Subgroup.id == subgroup_id).first()

def update_subgroup(db: Session, subgroup_id: int, name: str) -> Subgroup | None:
    db_subgroup = get_subgroup_by_id(db, subgroup_id)
    if db_subgroup:
        db_subgroup.name = name
        db.commit()
        db.refresh(db_subgroup)
    return db_subgroup

def delete_subgroup(db: Session, subgroup_id: int) -> Subgroup | None:
    db_subgroup = get_subgroup_by_id(db, subgroup_id)
    if db_subgroup:
        db.delete(db_subgroup)
        db.commit()
    return db_subgroup
