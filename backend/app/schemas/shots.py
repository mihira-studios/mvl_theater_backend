
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any

class ShotCreate(BaseModel):
    project_id: UUID
    sequence_id: UUID
    code: str
    name: Optional[str] = None
    status: str = "new"
    cutin: Optional[float] = None
    cutout: Optional[float] = None
    headin: Optional[float] = None
    tailout: Optional[float] = None
    meta: Dict[str, Any] = {}

class ShotOut(ShotCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
