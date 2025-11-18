
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class ProductCreate(BaseModel):
    project_id: UUID
    product_type_id: UUID
    user_id: UUID
    name: str
    status: str = "draft"
    asset_id: Optional[UUID] = None
    shot_id: Optional[UUID] = None
    task_id: Optional[UUID] = None

class ProductOut(ProductCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
