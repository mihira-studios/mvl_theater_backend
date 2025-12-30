from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.deps import get_db
from app.models.asset_shot_links import AssetShotLink
from app.models.assets import Asset
from app.models.shots import Shot
from app.schemas.asset_shot_links import AssetShotLinkCreate, AssetShotLinkRead


router = APIRouter(prefix="/asset-shot-links", tags=["AssetShotLinks"])


def _get_asset_or_404(db: Session, asset_id: UUID) -> Asset:
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


def _get_shot_or_404(db: Session, shot_id: UUID) -> Shot:
    shot = db.get(Shot, shot_id)
    if not shot:
        raise HTTPException(status_code=404, detail="Shot not found")
    return shot


@router.post(
    "",
    response_model=AssetShotLinkRead,
    status_code=status.HTTP_201_CREATED,
)
def create_link(
    payload: AssetShotLinkCreate,
    db: Session = Depends(get_db),
):
    # validate FK existence (optional but nice)
    _get_asset_or_404(db, payload.asset_id)
    _get_shot_or_404(db, payload.shot_id)

    link = AssetShotLink(
        asset_id=payload.asset_id,
        shot_id=payload.shot_id,
    )
    db.add(link)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # composite PK already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Link already exists",
        )

    db.refresh(link)
    return AssetShotLinkRead.model_validate(link)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_link(
    asset_id: UUID,
    shot_id: UUID,
    db: Session = Depends(get_db),
):
    link = (
        db.query(AssetShotLink)
        .filter(
            AssetShotLink.asset_id == asset_id,
            AssetShotLink.shot_id == shot_id,
        )
        .first()
    )

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return None


@router.get(
    "/by-asset/{asset_id}",
    response_model=List[AssetShotLinkRead],
)
def list_links_for_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    _get_asset_or_404(db, asset_id)

    links = (
        db.query(AssetShotLink)
        .filter(AssetShotLink.asset_id == asset_id)
        .order_by(AssetShotLink.created_at.desc())
        .all()
    )
    return [AssetShotLinkRead.model_validate(l) for l in links]


@router.get(
    "/by-shot/{shot_id}",
    response_model=List[AssetShotLinkRead],
)
def list_links_for_shot(
    shot_id: UUID,
    db: Session = Depends(get_db),
):
    _get_shot_or_404(db, shot_id)

    links = (
        db.query(AssetShotLink)
        .filter(AssetShotLink.shot_id == shot_id)
        .order_by(AssetShotLink.created_at.desc())
        .all()
    )
    return [AssetShotLinkRead.model_validate(l) for l in links]
