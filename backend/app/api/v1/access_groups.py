
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.access_groups import AccessGroup
from ...schemas.access_groups import AccessGroupOut, AccessGroupCreate

router = APIRouter()

@router.get("/", response_model=List[AccessGroupOut])
def list_access_groups(db: Session = Depends(get_db)):
    return db.query(AccessGroup).order_by(AccessGroup.created_at.desc()).all()

@router.post("/", response_model=AccessGroupOut, status_code=status.HTTP_201_CREATED)
def create_access_group(payload: AccessGroupCreate, db: Session = Depends(get_db)):
    existing = db.query(AccessGroup).filter(AccessGroup.name == payload.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Access group with this name already exists",
        )
    group = AccessGroup(name=payload.name, data=payload.data)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.get("/{group_id}", response_model=AccessGroupOut)
def get_access_group(group_id: UUID, db: Session = Depends(get_db)):
    group = db.query(AccessGroup).filter(AccessGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Access group not found")
    return group
