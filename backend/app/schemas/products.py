from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

from .versions import VersionCreate, VersionOut

class ProductCreate(BaseModel):
    project_id: UUID
    owner_kind: str = Field(..., description="asset | shot | task")
    owner_id: UUID
    product_type_id: UUID
    status: Optional[str] = "draft"
    created_by: UUID  # user id


class ProductCreateWithVersion(ProductCreate):
    version: VersionCreate


class ProductOut(BaseModel):
    id: UUID
    project_id: UUID
    owner_kind: str
    owner_id: UUID
    product_type_id: UUID
    status: str
    created_by: UUID
    created_at: str  # or datetime if you prefer

    class Config:
        from_attributes = True
