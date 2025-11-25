from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any

from .versions import VersionCreate  # import your updated VersionCreate


class ProductCreate(BaseModel):
    project_id: UUID
    product_type_id: UUID
    user_id: UUID
    name: str
    status: str = "draft"

    asset_id: Optional[UUID] = None
    shot_id: Optional[UUID] = None
    task_id: Optional[UUID] = None

    # optional extra info about the product, if your Product model has `meta`
    meta: Optional[Dict[str, Any]] = None


# Use this ONLY for endpoints that also create an initial version
class ProductCreateWithVersion(ProductCreate):
    version: VersionCreate


class ProductOut(ProductCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
