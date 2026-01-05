from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


# ---- Minimal nested read types ----
class SequenceMini(BaseModel):
    id: UUID
    project_id: UUID
    code: str
    name: Optional[str] = None
    status: str | None = None

    class Config:
        from_attributes = True


class AssetMini(BaseModel):
  

    id: UUID
    project_id: UUID
    code: str
    name: Optional[str] = None
    status: str = "new"

    class Config:
        from_attributes = True


class TaskMini(BaseModel):

    id: UUID
    project_id: UUID
    code: str
    name: Optional[str] = None
    status: str = "new"
    step_id: Optional[UUID] = None  # if your Task has steps etc.

    class Config:
        from_attributes = True

class ShotBase(BaseModel):
    code: str
    name: Optional[str] = None
    description: Optional[str] = None
    status: str = "new"

    cut_in: Optional[float] = None
    cut_out: Optional[float] = None
    cut_duration: Optional[float] = None

    head_in: Optional[float] = None
    head_out: Optional[float] = None
    head_duration: Optional[float] = None

    tail_in: Optional[float] = None
    tail_out: Optional[float] = None
    tail_duration: Optional[float] = None

    fps: Optional[float] = None
    cut_order: Optional[int] = None

    meta: Dict[str, Any] = Field(default_factory=dict)



class ShotCreate(ShotBase):
    project_id: UUID
    sequence_id: UUID
    asset_ids: List[UUID] = Field(default_factory=list)


class ShotUpdate(ShotBase):
    code: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    sequence_id: Optional[UUID] = None
    asset_ids: Optional[List[UUID]] = None


class ShotRead(ShotBase):
    
    id: UUID
    project_id: UUID
    sequence_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    sequence: Optional[SequenceMini] = None
    assets: List[AssetMini] = Field(default_factory=list)
    tasks: List[TaskMini] = Field(default_factory=list)

    class Config:
        from_attributes =True


class ShotOut(ShotRead):
    """Alias for response schema (naming consistency)."""
    pass