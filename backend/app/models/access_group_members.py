
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..db import Base

class AccessGroupMember(Base):
    __tablename__ = "access_group_members"

    access_group_id = Column(UUID(as_uuid=True), ForeignKey("access_groups.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String, nullable=False, default="member")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
