from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any, List, Literal


class VersionTags(BaseModel):
    usage: Optional[List[Literal["work", "publish", "client", "archive"]]] = None
    intent: Optional[Literal["wip", "preview", "final"]] = None

    class Config:
        extra = "allow"


class VersionCreate(BaseModel):
    product_id: UUID
    version: int
    status: str = "draft"
    notes: Optional[str] = None
    user_id: UUID

    # USD file
    path: str
    ext: str = "usd"

    # meta holds usd info + derived media:
    # {
    #   "usd": {...},
    #   "thumbnail": {...} (optional legacy),
    #   "playblast": {"path": "...", "ext": "mp4", "metadata": {...}}
    # }
    meta: Optional[Dict[str, Any]] = None

    # NEW thumbnail columns (preferred)
    thumbnail_path: Optional[str] = None
    thumbnail_ext: Optional[str] = "jpg"
    thumbnail_metadata: Optional[Dict[str, Any]] = None

    tags: Optional[VersionTags] = None


class VersionOut(VersionCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
