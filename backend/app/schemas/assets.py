
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any


class AssetCreate(BaseModel):
    project_id: UUID
    asset_category_id: UUID
    asset_type_id: UUID
    code: Optional[str] = None
    name: str = None
    status: str = "new"
    meta: Dict[str, Any] = {}

class AssetOut(AssetCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class AssetFromCSV(BaseModel):
    name: str
    status: str | None = None
    meta: dict
