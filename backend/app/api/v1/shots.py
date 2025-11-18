
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.shots import Shot
from ...schemas.shots import ShotOut, ShotCreate

router = APIRouter()

@router.get("/", response_model=List[ShotOut])
def list_shots(
    project_id: UUID | None = None,
    sequence_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Shot)
    if project_id:
        q = q.filter(Shot.project_id == project_id)
    if sequence_id:
        q = q.filter(Shot.sequence_id == sequence_id)
    return q.order_by(Shot.created_at.desc()).all()

@router.post("/", response_model=ShotOut)
def create_shot(payload: ShotCreate, db: Session = Depends(get_db)):
    shot = Shot(
        project_id=payload.project_id,
        sequence_id=payload.sequence_id,
        code=payload.code,
        name=payload.name,
        status=payload.status,
        cutin=payload.cutin,
        cutout=payload.cutout,
        headin=payload.headin,
        tailout=payload.tailout,
        meta=payload.meta,
    )
    db.add(shot)
    db.commit()
    db.refresh(shot)
    return shot
