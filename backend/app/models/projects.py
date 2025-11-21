
import uuid
from sqlalchemy import Column, Text, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from sqlalchemy.orm import relationship

from ..db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=True)
    status = Column(String, default="Active", nullable=False)
    archived = Column(Boolean, default=False, nullable=False)
    thumbnail = Column(String, nullable=True)
    config = Column(JSONB, default=dict, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    updated_by = Column(String, nullable=True)

