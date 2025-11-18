
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.representations import Representation
from ...schemas.representations import RepresentationOut, RepresentationCreate

router = APIRouter()

@router.get("/", response_model=List[RepresentationOut])
def list_representations(
    version_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Representation)
    if version_id:
        q = q.filter(Representation.version_id == version_id)
    return q.order_by(Representation.created_at.desc()).all()

@router.post("/", response_model=RepresentationOut)
def create_representation(payload: RepresentationCreate, db: Session = Depends(get_db)):
    rep = Representation(
        version_id=payload.version_id,
        name=payload.name,
        ext=payload.ext,
        path=payload.path,
        hash=payload.hash,
        size_bytes=payload.size_bytes,
    )
    db.add(rep)
    db.commit()
    db.refresh(rep)
    return rep
