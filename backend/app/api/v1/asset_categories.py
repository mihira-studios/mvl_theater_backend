
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.asset_categories import AssetCategory
from ...schemas.asset_categories import AssetCategoryOut, AssetCategoryCreate

router = APIRouter()

@router.get("/", response_model=List[AssetCategoryOut])
def list_asset_categories(
    project_id: UUID | None = None, db: Session = Depends(get_db)
):
    q = db.query(AssetCategory)
    if project_id:
        q = q.filter(AssetCategory.project_id == project_id)
    return q.order_by(AssetCategory.created_at.desc()).all()

@router.post("/", response_model=AssetCategoryOut)
def create_asset_category(payload: AssetCategoryCreate, db: Session = Depends(get_db)):
    cat = AssetCategory(
        project_id=payload.project_id,
        name=payload.name,
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat
