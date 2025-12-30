from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from .shots import ShotRead  # use the updated ShotRead


class SequenceBase(BaseModel):
    code: str
    name: Optional[str] = None
    status: str | None = None
    meta: Dict[str, Any] = Field(default_factory=dict)


class SequenceCreate(SequenceBase):
    project_id: UUID


class SequenceUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class SequenceRead(SequenceBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    shots: List[ShotRead] = Field(default_factory=list)

    class Config:
        from_attributes = True

class SequenceOut(SequenceRead):
    """Alias for response schema (naming consistency)."""
    pass