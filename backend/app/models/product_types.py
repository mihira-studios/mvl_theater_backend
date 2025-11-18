
from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..db import Base

class ProductType(Base):
    __tablename__ = "product_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    family = Column(String, nullable=True)
    scope = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("name", name="uq_product_type_name"),
    )
