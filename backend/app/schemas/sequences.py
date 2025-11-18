
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class SequenceCreate(BaseModel):
    project_id: UUID
    code: str
    name: Optional[str] = None

class SequenceOut(SequenceCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
