
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional

class TaskCreate(BaseModel):
    project_id: UUID
    name: str
    status: str = "todo"
    assignee_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    asset_id: Optional[UUID] = None
    shot_id: Optional[UUID] = None
    due_at: Optional[datetime] = None

class TaskOut(TaskCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
