from __future__ import annotations

from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError

from app.models.shots import Shot
from app.models.assets import Asset
from app.schemas.shots import ShotCreate, ShotUpdate, ShotRead


def to_shot_read(shot: Shot) -> ShotRead:
    """Convert ORM Shot -> Pydantic ShotRead/ShotOut."""
    return ShotRead.model_validate(shot)


def get_shot(
    db: Session,
    shot_id: UUID,
    with_related: bool = True,
) -> Shot | None:
    q = db.query(Shot)
    if with_related:
        q = q.options(
            selectinload(Shot.sequence),
            selectinload(Shot.assets),
            selectinload(Shot.tasks),
        )
    return q.filter(Shot.id == shot_id).first()


def get_shot_or_404(
    db: Session,
    shot_id: UUID,
    with_related: bool = True,
) -> Shot:
    shot = get_shot(db, shot_id, with_related=with_related)
    if not shot:
        raise ValueError("Shot not found")
    return shot


def list_shots(
    db: Session,
    project_id: UUID | None = None,
    sequence_id: UUID | None = None,
    with_related: bool = True,
) -> list[Shot]:
    q = db.query(Shot)

    if with_related:
        q = q.options(
            selectinload(Shot.sequence),
            selectinload(Shot.assets),
            selectinload(Shot.tasks),
        )

    if project_id:
        q = q.filter(Shot.project_id == project_id)

    if sequence_id is not None:
        q = q.filter(Shot.sequence_id == sequence_id)

    return q.order_by(Shot.code.asc()).all()


def create_shot(db: Session, payload: ShotCreate) -> Shot:
    data = payload.model_dump(exclude={"asset_ids"})
    asset_ids = payload.asset_ids

    shot = Shot(**data)

    if asset_ids:
        assets = db.query(Asset).filter(Asset.id.in_(asset_ids)).all()
        shot.assets = assets

    db.add(shot)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # likely uq_shot_code_per_project
        raise ValueError("Shot code already exists for this project.") from e

    db.refresh(shot)
    return shot


def update_shot(db: Session, shot: Shot, payload: ShotUpdate) -> Shot:
    data = payload.model_dump(exclude_unset=True, exclude={"asset_ids"})
    for k, v in data.items():
        setattr(shot, k, v)

    # Replace asset links if asset_ids intentionally provided
    if payload.asset_ids is not None:
        assets = db.query(Asset).filter(Asset.id.in_(payload.asset_ids)).all()
        shot.assets = assets

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Update would violate unique shot code per project.") from e

    db.refresh(shot)
    return shot


def delete_shot(db: Session, shot: Shot) -> None:
    db.delete(shot)
    db.commit()
