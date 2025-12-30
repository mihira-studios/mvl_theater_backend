
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any

class UserCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    active: bool = True
    attrib: Dict[str, Any] = {}
    data: Dict[str, Any] = {}

class UserOut(UserCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
