from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint, Index
# -------------------------
# Incoming data (Create)
# -------------------------
class ProjectCreate(BaseModel):
    name: str                          # Project Name
    code: str                          # Short code
    description: Optional[str] = None  # Description
    type: Optional[str] = None         # Type (Film, Game, Short, etc.)
    status: Optional[str] = "Active"   # Status field
    archived: bool = False             # Archived flag
    thumbnail: Optional[HttpUrl] = None  # Thumbnail image URL
    config: Dict[str, Any] = {}        # Custom pipeline config


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    archived: Optional[bool] = None
    thumbnail: Optional[HttpUrl] = None   # allow set or clear with null
    config: Optional[Dict[str, Any]] = None

# -------------------------
# Outgoing data (Read)
# -------------------------
class ProjectOut(ProjectCreate):
    id: UUID
    created_at: datetime               # Date Created
    updated_at: datetime               # Date Updated
    updated_by: Optional[str] = None   # Updated By (user email or name)

    class Config:
        from_attributes = True


class AddUserToProjectIn(BaseModel):
    project_id: UUID
    user_kc_id: str
    role: str  

class UpdateUserProjectRoleIn(BaseModel):
    role: str