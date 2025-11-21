
from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from ..db import Base

    
class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    asset_category_id = Column(UUID(as_uuid=True), ForeignKey("asset_categories.id", ondelete="RESTRICT"), nullable=False)
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id", ondelete="RESTRICT"), nullable=False)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=True)
    status = Column(Text, nullable=False, default="new")
    meta = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
