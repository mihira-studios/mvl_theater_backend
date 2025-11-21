
from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..db import Base

class AssetCategory(Base):
    __tablename__ = "asset_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("asset_type_id", "name", name="uq_asset_category_type_name"),
    )
