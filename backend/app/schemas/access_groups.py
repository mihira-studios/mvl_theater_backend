from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Dict, Any, Optional


class AccessGroupBase(BaseModel):
    name: str
    # Link to Keycloak group
    kc_group_id: str                      # Keycloak group UUID as string
    kc_group_path: Optional[str] = None   # e.g. "/engineering" (optional)
    data: Dict[str, Any] = Field(default_factory=dict)


class AccessGroupCreate(AccessGroupBase):
    """Payload used when creating a group."""
    pass

class AccessGroupUpdate(BaseModel):
    """Payload used for partial updates (PATCH)."""
    name: Optional[str] = None
    kc_group_id: Optional[str] = None
    kc_group_path: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class AccessGroupOut(AccessGroupBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
