from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import SiteCreate, SiteUpdate, SiteOut
from app.crud import site as crud_site
from app.database.db import get_db
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(
    prefix="/api/sites",
    tags=["sites"],
    dependencies=[Depends(get_current_user)],
    redirect_slashes=False
)

# Вспомогалка для приведения ORM -> Pydantic
def _to_out(obj) -> SiteOut:
    return SiteOut.from_orm(obj)

# --- Список объектов ---
@router.get("", response_model=list[SiteOut])
@router.get("/", response_model=list[SiteOut])
def read_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = crud_site.get_sites(db, current_user.id)
    return [_to_out(x) for x in items]

# --- Создание объекта ---
@router.post("", response_model=SiteOut)
@router.post("/", response_model=SiteOut)
def create_site(
    site: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    created = crud_site.create_site(db, site, current_user.id)
    return _to_out(created)

# --- Получение конкретного объекта ---
@router.get("/{site_id}", response_model=SiteOut)
def read_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_site = crud_site.get_site(db, site_id)
    if not db_site or db_site.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site not found")
    return _to_out(db_site)

# --- Удаление объекта ---
@router.delete("/{site_id}")
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = crud_site.delete_site(db, site_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"message": "Site deleted successfully"}

# --- Архивирование объекта ---
@router.post("/{site_id}/archive")
def archive_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = crud_site.archive_site(db, site_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Site not found")
    return {"message": "Site archived successfully"}

# --- Список архивных объектов ---
@router.get("/archive", response_model=list[SiteOut])
def read_archived_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = crud_site.get_sites(db, current_user.id, include_archived=True)
    return [_to_out(x) for x in items]

# --- Обновление объекта ---
@router.put("/{site_id}", response_model=SiteOut)
def update_site(
    site_id: int,
    site: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = crud_site.update_site(db, site_id, site)
    if updated is None or updated.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Site not found")
    return _to_out(updated)
