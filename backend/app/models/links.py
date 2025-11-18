
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from ..db import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    link_kind = Column(String, nullable=False)
    scope = Column(String, nullable=True)
    src_kind = Column(String, nullable=False)
    src_id = Column(UUID(as_uuid=True), nullable=False)
    dst_kind = Column(String, nullable=False)
    dst_id = Column(UUID(as_uuid=True), nullable=False)
    meta = Column(JSONB, default=dict, nullable=False)
