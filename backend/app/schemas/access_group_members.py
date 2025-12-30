from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Optional


class AccessGroupMemberBase(BaseModel):
    user_kc_id: str          # Keycloak user id (token.sub)
    access_group_id: UUID    # FK to access_groups.id


class AccessGroupMemberCreate(AccessGroupMemberBase):
    """Payload for adding a user to an access group."""
    pass


class AccessGroupMemberOut(AccessGroupMemberBase):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AccessGroupMemberDelete(BaseModel):
    """Payload if you want an explicit delete body (optional)."""
    user_kc_id: str
    access_group_id: UUID
