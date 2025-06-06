from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import SiteCreate, Site
from app.crud import site as crud_site
from app.database.db import get_db
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/sites", tags=["Sites"])

@router.post("/", response_model=Site)
def create_site(
    site: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_site.create_site(db, site, current_user.id)

@router.get("/", response_model=list[Site])
def read_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_site.get_sites(db, current_user.id)

@router.get("/{site_id}", response_model=Site)
def read_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_site = crud_site.get_site(db, site_id, current_user.id)
    if db_site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return db_site

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
