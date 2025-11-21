
from sqlalchemy import Column, String, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from ..db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(UUID(as_uuid=True), unique=True, nullable=True)
    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(Text, unique=True, nullable=False)
    attrib = Column(JSONB, default=dict, nullable=False)
    data = Column(JSONB, default=dict, nullable=False)
    contact = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class UserAccessGroup(Base):
    __tablename__ = "user_access_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    access_group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("access_groups.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "access_group_id", name="uq_user_group"),
    )

    # Optional:
    # user = relationship("User", backref="group_links")
    # access_group = relationship("AccessGroup", backref="user_links")

