
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..db import Base

class Representation(Base):
    __tablename__ = "representations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id = Column(UUID(as_uuid=True), ForeignKey("versions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=True)
    ext = Column(String, nullable=False)
    path = Column(Text, nullable=False)
    hash = Column(String, nullable=True)
    size_bytes = Column(BigInteger, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
