from sqlalchemy import Column, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..db import Base


class Sequence(Base):
    __tablename__ = "sequences"

    __table_args__ = (
        UniqueConstraint("project_id", "code", name="uq_sequence_code_per_project"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    code = Column(Text, nullable=False)
    name = Column(Text, nullable=True)
    status = Column(Text, nullable=False, default="new")

    meta = Column(JSONB, default=dict, nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    shots = relationship(
        "Shot",
        back_populates="sequence",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Shot.code",
    )
