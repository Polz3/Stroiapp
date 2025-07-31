from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas.schemas import SiteCreate, Site, SiteUpdate  # Site = наш SiteOut
from app.crud import site as crud_site
from app.database.db import get_db  # ← вот так
from app.api.auth import get_current_user
from app.models.models import User

router = APIRouter(
    prefix="/api/sites",
    tags=["sites"],
    dependencies=[Depends(get_current_user)]  
)


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
    db_site = crud_site.get_site(db, site_id)
    if not db_site or db_site.user_id != current_user.id:
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


@router.get("/archive", response_model=list[Site])
def read_archived_sites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_site.get_sites(db, current_user.id, include_archived=True)

@router.put("/{site_id}", response_model=Site)
def update_site(
    site_id: int,
    site: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = crud_site.update_site(db, site_id, site)
    if updated is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return updated
