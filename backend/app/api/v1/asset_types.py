
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.asset_types import AssetType
from ...schemas.asset_types import AssetTypeOut, AssetTypeCreate

router = APIRouter()

@router.get("/", response_model=List[AssetTypeOut])
def list_asset_types(
    project_id: UUID | None = None, db: Session = Depends(get_db)
):
    q = db.query(AssetType)
    if project_id:
        q = q.filter(AssetType.project_id == project_id)
    return q.order_by(AssetType.created_at.desc()).all()

@router.post("/", response_model=AssetTypeOut)
def create_asset_type(payload: AssetTypeCreate, db: Session = Depends(get_db)):
    at = AssetType(
        project_id=payload.project_id,
        asset_category_id=payload.asset_category_id,
        name=payload.name,
    )
    db.add(at)
    db.commit()
    db.refresh(at)
    return at
