
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    ver = Version(
        product_id=payload.product_id,
        version=payload.version,
        status=payload.status,
        notes=payload.notes,
        user_id=payload.user_id,
    )
    db.add(ver)
    db.commit()
    db.refresh(ver)
    return ver
