
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Dict, Any

class AccessGroupCreate(BaseModel):
    name: str
    data: Dict[str, Any] = {}

class AccessGroupOut(AccessGroupCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
