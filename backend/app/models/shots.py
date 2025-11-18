
from sqlalchemy import Column, DateTime, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from ..db import Base

class Shot(Base):
    __tablename__ = "shots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    sequence_id = Column(UUID(as_uuid=True), ForeignKey("sequences.id", ondelete="CASCADE"), nullable=False)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=True)
    status = Column(Text, nullable=False, default="new")
    cutin = Column(Float, nullable=True)
    cutout = Column(Float, nullable=True)
    headin = Column(Float, nullable=True)
    tailout = Column(Float, nullable=True)
    meta = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
