
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AssetCategoryCreate(BaseModel):
    asset_type_id: UUID
    name: str

class AssetCategoryOut(AssetCategoryCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
