# access_group_members.py
from sqlalchemy import Column, DateTime, ForeignKey, String, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..db import Base

class AccessGroupMember(Base):
    __tablename__ = "access_group_members"
    __table_args__ = (
        UniqueConstraint("user_kc_id", "access_group_id", name="uq_user_group"),
    )
    
    user_kc_id = Column(String, primary_key=True)  # Keycloak sub
    access_group_id = Column(UUID(as_uuid=True),
                             ForeignKey("access_groups.id", ondelete="CASCADE"),
                             primary_key=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    #group = relationship("AccessGroup", back_populates="members")

