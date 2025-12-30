from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError

from app.models.sequences import Sequence
from app.schemas.sequences import SequenceCreate, SequenceUpdate, SequenceRead


def to_sequence_read(seq: Sequence) -> SequenceRead:
    """Convert ORM -> Pydantic read schema."""
    return SequenceRead.model_validate(seq)


def get_sequence_or_404(
    db: Session,
    sequence_id: UUID,
    with_shots: bool = True,
) -> Sequence | None:
    q = db.query(Sequence)
    if with_shots:
        q = q.options(selectinload(Sequence.shots))

    return q.filter(Sequence.id == sequence_id).first()


def list_sequences(
    db: Session,
    project_id: UUID | None = None,
    with_shots: bool = False,
) -> list[Sequence]:
    q = db.query(Sequence)
    if with_shots:
        q = q.options(selectinload(Sequence.shots))
    if project_id:
        q = q.filter(Sequence.project_id == project_id)

    return q.order_by(Sequence.code.asc()).all()


def create_sequence(db: Session, payload: SequenceCreate) -> Sequence:
    seq = Sequence(
        project_id=payload.project_id,
        code=payload.code,
        name=payload.name,
        status=payload.status,
        meta=payload.meta,
    )
    db.add(seq)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # likely uq_sequence_code_per_project
        raise ValueError("Sequence code already exists for this project.") from e

    db.refresh(seq)
    return seq


def update_sequence(db: Session, seq: Sequence, payload: SequenceUpdate) -> Sequence:
    data = payload.model_dump(exclude_unset=True)

    for k, v in data.items():
        setattr(seq, k, v)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Update would violate unique code per project.") from e

    db.refresh(seq)
    return seq


def delete_sequence(db: Session, seq: Sequence) -> None:
    db.delete(seq)
    db.commit()
