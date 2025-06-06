from sqlalchemy.orm import Session
from app.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate

def get_materials(db: Session, user_id: int, skip=0, limit=100, include_archived=False):
    q = db.query(Material).filter(Material.user_id == user_id)
    if not include_archived:
        q = q.filter(Material.is_archived == False)
    return q.offset(skip).limit(limit).all()

def get_material(db: Session, material_id: int) -> Material | None:
    return db.query(Material).filter(Material.id == material_id).first()

def create_material(db: Session, material: MaterialCreate) -> Material:
    db_mat = Material(**material.model_dump(), is_archived=False)
    db.add(db_mat)
    db.commit()
    db.refresh(db_mat)
    return db_mat

def update_material(db: Session, material_id: int, mat_update: MaterialUpdate) -> Material | None:
    db_mat = get_material(db, material_id)
    if not db_mat:
        return None
    data = mat_update.model_dump(exclude_unset=True)
    for f, v in data.items():
        setattr(db_mat, f, v)
    db.commit()
    db.refresh(db_mat)
    return db_mat

def delete_material(db: Session, material_id: int) -> bool:
    db_mat = get_material(db, material_id)
    if not db_mat:
        return False
    db.delete(db_mat)
    db.commit()
    return True

def archive_material(db: Session, material_id: int) -> Material | None:
    db_mat = get_material(db, material_id)
    if not db_mat:
        return None
    db_mat.is_archived = True
    db.commit()
    db.refresh(db_mat)
    return db_mat

def restore_material(db: Session, material_id: int) -> Material | None:
    db_mat = get_material(db, material_id)
    if not db_mat:
        return None
    db_mat.is_archived = False
    db.commit()
    db.refresh(db_mat)
    return db_mat
