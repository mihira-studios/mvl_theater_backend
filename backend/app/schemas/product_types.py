
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ProductTypeCreate(BaseModel):
    name: str
    family: Optional[str] = None
    scope: Optional[str] = None

class ProductTypeOut(ProductTypeCreate):
    id: UUID

    class Config:
        from_attributes = True
