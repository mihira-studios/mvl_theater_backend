from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any


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


# -------------------------
# Outgoing data (Read)
# -------------------------
class ProjectOut(ProjectCreate):
    id: UUID
    created_at: datetime               # Date Created
    updated_at: datetime               # Date Updated
    updated_by: Optional[str] = None   # Updated By (user email or name)

    class Config:
        orm_mode = True
