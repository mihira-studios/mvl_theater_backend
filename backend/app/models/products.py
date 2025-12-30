
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, CheckConstraint, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    project_id = Column(UUID(as_uuid=True),
                        ForeignKey("projects.id", ondelete="CASCADE"),
                        nullable=False)

    owner_kind = Column(String, nullable=False)  # 'asset'/'shot'/'task'
    owner_id = Column(UUID(as_uuid=True), nullable=False)

    product_type_id = Column(UUID(as_uuid=True),
                             ForeignKey("product_types.id", ondelete="RESTRICT"),
                             nullable=False)

    status = Column(String, nullable=False, default="draft")

    created_by = Column(UUID(as_uuid=True),
                        ForeignKey("users.id", ondelete="RESTRICT"),
                        nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint("owner_kind IN ('asset','shot','task')", name="products_owner_kind_chk"),
        UniqueConstraint("project_id", "owner_kind", "owner_id", "product_type_id",
                         name="uniq_products_owner_type"),
        Index("idx_products_owner", "owner_kind", "owner_id"),
        Index("idx_products_project", "project_id"),
    )

