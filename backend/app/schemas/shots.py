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


# ---- Base / Create / Update ----
class ShotBase(BaseModel):
    code: str
    name: Optional[str] = None
    status: str = "new"
    meta: Dict[str, Any] = Field(default_factory=dict)


class ShotCreate(ShotBase):
    project_id: UUID
    sequence_id: Optional[UUID] = None

    # optional: allow setting asset links at create
    asset_ids: List[UUID] = Field(default_factory=list)


class ShotUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    sequence_id: Optional[UUID] = None

    # optional: replace asset links via PATCH
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