
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.sequences import Sequence
from ...schemas.sequences import SequenceOut, SequenceCreate

router = APIRouter()

@router.get("/", response_model=List[SequenceOut])
def list_sequences(
    project_id: UUID | None = None, db: Session = Depends(get_db)
):
    q = db.query(Sequence)
    if project_id:
        q = q.filter(Sequence.project_id == project_id)
    return q.order_by(Sequence.created_at.desc()).all()

@router.post("/", response_model=SequenceOut)
def create_sequence(payload: SequenceCreate, db: Session = Depends(get_db)):
    seq = Sequence(
        project_id=payload.project_id,
        code=payload.code,
        name=payload.name,
    )
    db.add(seq)
    db.commit()
    db.refresh(seq)
    return seq
