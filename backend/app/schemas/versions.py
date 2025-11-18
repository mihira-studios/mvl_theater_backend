
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class VersionCreate(BaseModel):
    product_id: UUID
    version: int
    status: str = "draft"
    notes: Optional[str] = None
    user_id: UUID

class VersionOut(VersionCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
