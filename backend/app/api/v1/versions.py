from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.resolver import (
    next_version_number,
)
from ...deps import get_db
from ...models.versions import Version
from ...schemas.versions import VersionOut, VersionCreate

router = APIRouter()


@router.get("/", response_model=List[VersionOut])
def list_versions(
    product_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Version)

    if product_id:
        q = q.filter(Version.product_id == product_id)

    return q.order_by(Version.created_at.desc()).all()


@router.post("/", response_model=VersionOut)
def create_version(payload: VersionCreate, db: Session = Depends(get_db)):
    ver_num = next_version_number(db, payload.product_id)

    ver = Version(
        product_id=payload.product_id,
        version=ver_num,  # auto

        status=payload.status,
        notes=payload.notes,
        user_id=payload.user_id,

        path=payload.path,
        ext=payload.ext,
        meta=payload.meta,

        thumbnail_path=payload.thumbnail_path,
        thumbnail_ext=payload.thumbnail_ext,
        thumbnail_metadata=payload.thumbnail_metadata,

        tags=payload.tags.dict() if payload.tags else None,
    )

    db.add(ver)
    db.commit()
    db.refresh(ver)
    return ver

