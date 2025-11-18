
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class AssetTypeCreate(BaseModel):
    project_id: UUID
    asset_category_id: UUID
    name: str

class AssetTypeOut(AssetTypeCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
