
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.assets import Asset
from ...schemas.assets import AssetOut, AssetCreate

router = APIRouter()

@router.get("/", response_model=List[AssetOut])
def list_assets(
    project_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Asset)
    if project_id:
        q = q.filter(Asset.project_id == project_id)
    return q.order_by(Asset.created_at.desc()).all()

@router.post("/", response_model=AssetOut)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        project_id=payload.project_id,
        asset_category_id=payload.asset_category_id,
        asset_type_id=payload.asset_type_id,
        code=payload.code,
        name=payload.name,
        status=payload.status,
        meta=payload.meta,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
