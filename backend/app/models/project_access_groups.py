
from sqlalchemy import Column, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..db import Base

class ProjectAccessGroup(Base):
    __tablename__ = "project_access_groups"


    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key= True,
    )
    access_group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("access_groups.id", ondelete="CASCADE"),
        primary_key= True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)