from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.shots import ShotCreate, ShotUpdate, ShotOut
from app.core.crud import (
    get_shot,
    list_shots,
    create_shot,
    update_shot,
    delete_shot,
    to_shot_read,        # optional helper
    get_shot_or_404,     # optional helper
)

router = APIRouter()

@router.post(
    "",
    response_model=ShotOut,
    status_code=status.HTTP_201_CREATED,
)
def create_shot_endpoint(
    payload: ShotCreate,
    db: Session = Depends(get_db),
):
    try:
        shot = create_shot(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return ShotOut.model_validate(shot)


@router.get(
    "/{shot_id}",
    response_model=ShotOut,
)
def get_shot_endpoint(
    shot_id: UUID,
    db: Session = Depends(get_db),
):
    shot = get_shot(db, shot_id, with_related=True)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")
    return ShotOut.model_validate(shot)


@router.get(
    "",
    response_model=list[ShotOut],
)
def list_shots_endpoint(
    project_id: UUID | None = None,
    sequence_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    shots = list_shots(
        db,
        project_id=project_id,
        sequence_id=sequence_id,
        with_related=True,
    )
    return [ShotOut.model_validate(s) for s in shots]


@router.patch(
    "/{shot_id}",
    response_model=ShotOut,
)
def patch_shot_endpoint(
    shot_id: UUID,
    payload: ShotUpdate,
    db: Session = Depends(get_db),
):
    shot = get_shot(db, shot_id, with_related=False)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")

    try:
        shot = update_shot(db, shot, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    # re-fetch with relations for response
    shot = get_shot(db, shot_id, with_related=True)
    return ShotOut.model_validate(shot)


@router.delete(
    "/{shot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_shot_endpoint(
    shot_id: UUID,
    db: Session = Depends(get_db),
):
    shot = get_shot(db, shot_id, with_related=False)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")

    delete_shot(db, shot)
    return None
