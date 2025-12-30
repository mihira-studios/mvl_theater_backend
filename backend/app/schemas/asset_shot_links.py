from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AssetShotLinkBase(BaseModel):
    asset_id: UUID
    shot_id: UUID


class AssetShotLinkCreate(AssetShotLinkBase):
    """Payload to create a link."""
    pass


class AssetShotLinkRead(AssetShotLinkBase):
    """Response model."""
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime


class AssetShotLinkDelete(AssetShotLinkBase):
    """Payload to create a link."""
    pass

class AssetShotLinkOut(AssetShotLinkRead):
    pass