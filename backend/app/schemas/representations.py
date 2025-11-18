
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class RepresentationCreate(BaseModel):
    version_id: UUID
    ext: str
    path: str
    name: Optional[str] = None
    hash: Optional[str] = None
    size_bytes: int = 0

class RepresentationOut(RepresentationCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
