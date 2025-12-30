import uuid
from datetime import datetime
from sqlalchemy import Column, Text, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from ..db import Base


class Shot(Base):
    __tablename__ = "shots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(UUID(as_uuid=True),
                        ForeignKey("projects.id", ondelete="CASCADE"),
                        nullable=False)

    sequence_id = Column(UUID(as_uuid=True),
                         ForeignKey("sequences.id", ondelete="CASCADE"),
                         nullable=False)

    code = Column(Text, nullable=False)                  # SH010
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

    status = Column(Text, nullable=False, default="new")

    # Editorial timing (frames or seconds; your choice)
    cut_in = Column(Float, nullable=True)
    cut_out = Column(Float, nullable=True)
    cut_duration = Column(Float, nullable=True)

    head_in = Column(Float, nullable=True)
    head_out = Column(Float, nullable=True)
    head_duration = Column(Float, nullable=True)

    tail_in = Column(Float, nullable=True)
    tail_out = Column(Float, nullable=True)
    tail_duration = Column(Float, nullable=True)

    fps = Column(Float, nullable=True)                  # sg_mvl_fps
    cut_order = Column(Integer, nullable=True)          # sg_cut_order

    # Everything else from CSV lives here
    meta = Column(JSONB, default=dict, nullable=False)

    created_by = Column(UUID(as_uuid=True),
                        ForeignKey("users.id", ondelete="SET NULL"),
                        nullable=True)

    updated_by = Column(UUID(as_uuid=True),
                        ForeignKey("users.id", ondelete="SET NULL"),
                        nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    # ---------------- Relationships (from multi_entity fields) ----------------
    sequence = relationship(
        "Sequence",
        back_populates="shots",
        passive_deletes=True,
    )
    
    assets = relationship(
        "Asset",
        secondary="asset_shot_links",
        back_populates="shots",
        passive_deletes=True,
    )

    tasks = relationship(
        "Task",
        back_populates="shot",
        passive_deletes=True,
    )

    
