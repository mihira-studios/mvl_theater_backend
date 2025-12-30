
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID

from typing import Optional

class AssetCategoryCreate(BaseModel):
    asset_type_id: UUID
    name: str
    default_thumbnail_path: Optional[HttpUrl] = None  # can store URL or relative path

class AssetCategoryOut(AssetCategoryCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
