from sqlalchemy.orm import Session, joinedload
from app.models.models import Site
from app.models.salary import Salary
from app.schemas.schemas import SiteCreate, SiteUpdate
from typing import Optional


def get_sites(
    db: Session,
    user_id: Optional[int] = None,
    search: str = "",
    subgroup_id: Optional[int] = None,
    include_archived: Optional[bool] = False
):
    query = db.query(Site)

    if user_id is not None:
        query = query.filter(Site.user_id == user_id)

    if include_archived is False:
        query = query.filter(Site.is_archived == False)
    elif include_archived is True:
        query = query.filter(Site.is_archived == True)

    if search:
        query = query.filter(Site.name.ilike(f"%{search}%"))
    if subgroup_id:
        query = query.filter(Site.subgroup_id == subgroup_id)

    return query.order_by(Site.id.desc()).all()


def get_site(db: Session, site_id: int, user_id: Optional[int] = None):
    query = db.query(Site).options(joinedload(Site.subgroup)).filter(Site.id == site_id)
    if user_id is not None:
        query = query.filter(Site.user_id == user_id)
    return query.first()


def create_site(db: Session, site: SiteCreate, user_id: int):
    db_site = Site(
        name=site.name,
        address=site.address,
        user_id=user_id
    )
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site


def update_site(db: Session, site_id: int, site: SiteUpdate, user_id: Optional[int] = None):
    query = db.query(Site).filter(Site.id == site_id)
    if user_id is not None:
        query = query.filter(Site.user_id == user_id)
    db_site = query.first()
    if db_site:
        db_site.name = site.name
        db_site.address = site.address
        db_site.subgroup_id = site.subgroup_id
        db.commit()
        db.refresh(db_site)
    return db_site


def archive_site(db: Session, site_id: int, user_id: int):
    site = db.query(Site).filter(Site.id == site_id, Site.user_id == user_id).first()
    if site:
        site.is_archived = True
        db.commit()
        return True
    return False


def restore_site(db: Session, site_id: int, user_id: Optional[int] = None):
    query = db.query(Site).filter(Site.id == site_id)
    if user_id is not None:
        query = query.filter(Site.user_id == user_id)
    site = query.first()
    if site:
        site.is_archived = False
        db.commit()


def delete_site(db: Session, site_id: int, user_id: int):
    site = db.query(Site).filter(Site.id == site_id, Site.user_id == user_id).first()
    if site:
        db.delete(site)
        db.commit()
        return True
    return False


def get_sites_by_worker(db: Session, worker_id: int, user_id: Optional[int] = None) -> list[Site]:
    site_ids_query = db.query(Salary.site_id).filter(Salary.worker_id == worker_id).distinct()
    if user_id is not None:
        site_ids_query = site_ids_query.filter(Salary.user_id == user_id)
    site_ids = site_ids_query.subquery()
    return db.query(Site).filter(Site.id.in_(site_ids)).all()
