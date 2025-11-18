
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Dict, Any

class ProjectCreate(BaseModel):
    name: str
    code: str
    library: bool = False
    active: bool = True
    config: Dict[str, Any] = {}

class ProjectOut(ProjectCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
