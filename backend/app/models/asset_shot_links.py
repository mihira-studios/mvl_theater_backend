from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class AssetShotLink(Base):
    __tablename__ = "asset_shot_links"

    asset_id = Column(UUID(as_uuid=True),
                      ForeignKey("assets.id", ondelete="CASCADE"),
                      nullable=False)

    shot_id = Column(UUID(as_uuid=True),
                     ForeignKey("shots.id", ondelete="CASCADE"),
                     nullable=False)

    created_at = Column(DateTime(timezone=True),
                        default=datetime.utcnow,
                        nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("asset_id", "shot_id", name="asset_shot_links_pkey"),
    )
