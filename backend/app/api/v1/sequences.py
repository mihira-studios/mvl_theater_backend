from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from ...deps import get_db
from app.models import Sequence
from app.schemas.sequences import SequenceCreate, SequenceUpdate, SequenceRead
from  app.core.crud import (
    create_sequence,
    update_sequence,
    get_sequence_or_404,
    to_sequence_read,
)

router = APIRouter()


@router.post("", response_model=SequenceRead, status_code=status.HTTP_201_CREATED)
def create_sequence_endpoint(payload: SequenceCreate, db: Session = Depends(get_db)):
    try:
        seq = create_sequence(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return to_sequence_read(seq)


@router.get("/{sequence_id}", response_model=SequenceRead)
def get_sequence_endpoint(sequence_id: UUID, db: Session = Depends(get_db)):
    # eager load shots for this one sequence
    seq = (
        db.query(Sequence)
        .options(selectinload(Sequence.shots))
        .filter(Sequence.id == sequence_id)
        .first()
    )
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return to_sequence_read(seq)


@router.get("", response_model=list[SequenceRead])
def list_sequences_endpoint(project_id: UUID | None = None, db: Session = Depends(get_db)):
    q = db.query(Sequence).options(selectinload(Sequence.shots))
    if project_id:
        q = q.filter(Sequence.project_id == project_id)

    seqs = q.order_by(Sequence.code.asc()).all()
    return [to_sequence_read(s) for s in seqs]


@router.patch("/{sequence_id}", response_model=SequenceRead)
def patch_sequence_endpoint(sequence_id: UUID, payload: SequenceUpdate, db: Session = Depends(get_db)):
    seq = get_sequence_or_404(db, sequence_id)
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")

    try:
        seq = update_sequence(db, seq, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    # optional: reload shots for response if your update doesn't touch them
    db.refresh(seq)
    return to_sequence_read(seq)


@router.delete("/{sequence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sequence_endpoint(sequence_id: UUID, db: Session = Depends(get_db)):
    seq = get_sequence_or_404(db, sequence_id)
    if not seq:
        raise HTTPException(status_code=404, detail="Sequence not found")

    db.delete(seq)
    db.commit()
    return None
