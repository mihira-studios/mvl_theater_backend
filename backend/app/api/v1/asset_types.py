from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.asset_types import AssetType
from ...schemas.asset_types import AssetTypeOut, AssetTypeCreate

router = APIRouter()


@router.get("/", response_model=List[AssetTypeOut])
def list_asset_types(
    db: Session = Depends(get_db)
):
    return (
        db.query(AssetType)
        .order_by(AssetType.created_at.desc())
        .all()
    )


@router.post("/", response_model=AssetTypeOut, status_code=status.HTTP_201_CREATED)
def create_asset_type(
    payload: AssetTypeCreate,
    db: Session = Depends(get_db)
):
    # Prevent duplicate names
    existing = (
        db.query(AssetType)
        .filter(AssetType.name.ilike(payload.name))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Asset type '{payload.name}' already exists",
        )

    at = AssetType(
        name=payload.name,
        # created_at is auto-set by the model default
    )

    db.add(at)
    db.commit()
    db.refresh(at)
    return at
