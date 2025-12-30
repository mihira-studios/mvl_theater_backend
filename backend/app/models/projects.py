
import uuid
from sqlalchemy import (
    Column, 
    Text, 
    String, 
    Boolean, 
    DateTime, 
    ForeignKey, 
    UniqueConstraint, 
    Index)
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

class UserProjectAccess(Base):
    __tablename__ = "user_project"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Keycloak user id (token.sub)
    user_kc_id = Column(String, nullable=False)

    # e.g. viewer/artist/lead/producer/admin (or project-scoped if you want)
    role = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        # one role per user per project
        UniqueConstraint("project_id", "user_kc_id", name="uq_user_projects"),
        # helpful index for "my projects"
        Index("ix_user_project_user_kc_id", "user_kc_id"),
        Index("ix_user_project_project_id", "project_id"),
    )
