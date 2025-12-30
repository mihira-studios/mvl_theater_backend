
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from ...deps import get_db
from ...models.projects import Project, UserProjectAccess
from ...models.sequences import Sequence
from ...schemas.projects import (
    ProjectOut, 
    ProjectCreate, 
    ProjectUpdate,
    AddUserToProjectIn,
    UpdateUserProjectRoleIn)
from app.core.auth.auth import verify_keycloak_token

router = APIRouter()

@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    existing = db.query(Project).filter(Project.code == payload.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project code already exists",
        )

    project = Project(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        type=payload.type,
        status=payload.status,
        archived=payload.archived,
        thumbnail=str(payload.thumbnail) if payload.thumbnail else None,
        config=payload.config,
        # active, created_at, updated_at, updated_by can rely on model defaults
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
):
    project = db.query(Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        # scalar fields
        if payload.name is not None:
            project.name = payload.name

        if payload.code is not None:
            # check unique code
            dup = (
                db.query(Project)
                .filter(Project.code.ilike(payload.code), Project.id != project_id)
                .first()
            )
            if dup:
                raise HTTPException(status_code=409, detail="Project code already exists")
            project.code = payload.code

        if payload.description is not None:
            project.description = payload.description

        if payload.type is not None:
            project.type = payload.type

        if payload.status is not None:
            project.status = payload.status

        if payload.archived is not None:
            project.archived = payload.archived

        # thumbnail (can be set or cleared)
        if payload.thumbnail is not None:
            project.thumbnail = str(payload.thumbnail)
        elif "thumbnail" in payload.__fields_set__:
            # explicitly sent null => clear it
            project.thumbnail = None

        # config merge (PATCH behavior)
        if payload.config is not None:
            project.config = _merge_json(project.config, payload.config)

        # updated_by if you want to pass from auth later
        # project.updated_by = current_user.email

        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to update project: {e}")

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.get("/{project_id}/sequences/count")
def get_sequence_count(project_id: UUID, db: Session = Depends(get_db)):
    #optional: ensure project exists
    exists = db.query(Project.id).filter(Project.id == project_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")

    count = (
        db.query(func.count(Sequence.id))
        .filter(Sequence.project_id == project_id)
        .scalar()
    )
    return {"project_id": project_id, "sequence_count": int(count)}

@router.get("/{project_id}/sequences")
def get_project_sequences(project_id: UUID, db: Session = Depends(get_db)):
    # optional: ensure project exists
    exists = db.query(Project.id).filter(Project.id == project_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")

    sequences = (
        db.query(Sequence)
        .filter(Sequence.project_id == project_id)
        .order_by(Sequence.code)
        .all()
    )
    
    return [
        {
            "id": str(s.id),
            "project_id": str(s.project_id),
            "code": s.code,
            "name": s.name,
            "status": s.status,
            "meta": s.meta,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
        }
        for s in sequences
    ]

@router.get("/{project_id}/shots/count")
def get_project_shot_count(project_id: UUID, db: Session = Depends(get_db)):
    exists = db.query(Project.id).filter(Project.id == project_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")

    shots_text = Sequence.meta["shots"].astext  # meta->>'shots'

    # Turn "shot1, shot2" into array ["shot1","shot2"] (handles spaces around commas)
    shots_array = func.regexp_split_to_array(
        func.nullif(func.btrim(shots_text), ""),   # empty string -> NULL
        r"\s*,\s*"
    )

    total = (
        db.query(
            func.coalesce(
                func.sum(func.coalesce(func.array_length(shots_array, 1), 0)),
                0
            )
        )
        .filter(Sequence.project_id == project_id)
        .scalar()
    )

    return {"project_id": project_id, "shot_count": int(total)}

@router.post("/access")
def add_user_to_project(payload: AddUserToProjectIn, user=Depends(verify_keycloak_token), db: Session = Depends(get_db)):
    # (Optional) authorize: only project admins can add users
    # TODO: enforce your policy here

    # Ensure project exists (nice error)
    exists = db.query(Project.id).filter(Project.id == payload.project_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="Project not found")

    row = UserProjectAccess(
        project_id=payload.project_id,
        user_kc_id=payload.user_kc_id,
        role=payload.role,
    )
    db.add(row)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # UniqueConstraint(project_id, user_kc_id) hit
        raise HTTPException(status_code=409, detail="User already has access to this project")

    db.refresh(row)
    return {
        "id": str(row.id),
        "project_id": str(row.project_id),
        "user_kc_id": row.user_kc_id,
        "role": row.role,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }

@router.put("/projects/{project_id}/users/{user_kc_id}")
def update_user_role(
    project_id: UUID,
    user_kc_id: str,
    payload: UpdateUserProjectRoleIn,
    user=Depends(verify_keycloak_token),
    db: Session = Depends(get_db),
):
    # (Optional) authorize: only project admins can change roles
    # TODO: enforce your policy here

    row = (
        db.query(UserProjectAccess)
          .filter(
              UserProjectAccess.project_id == project_id,
              UserProjectAccess.user_kc_id == user_kc_id,
          )
          .one_or_none()
    )
    if not row:
        raise HTTPException(status_code=404, detail="User access not found for this project")

    row.role = payload.role
    db.commit()
    db.refresh(row)

    return {
        "id": str(row.id),
        "project_id": str(row.project_id),
        "user_kc_id": row.user_kc_id,
        "role": row.role,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }