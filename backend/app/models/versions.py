from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..db import Base

class Version(Base):
    __tablename__ = "versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    version = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="draft")
    notes = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)

    # main USD file for this version
    path = Column(Text, nullable=False)
    ext = Column(String, nullable=False, default="usd")
    meta = Column(JSONB, nullable=True)   # info about the USD

    thumbnail_path = Column(Text, nullable=True)
    thumbnail_ext = Column(String, nullable=True, default="svg")
    thumbnail_metadata = Column(JSONB, nullable=True) 

    tags = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("product_id", "version", name="uq_product_version"),
    )
