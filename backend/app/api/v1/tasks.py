
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.tasks import Task
from ...schemas.tasks import TaskOut, TaskCreate

router = APIRouter()

@router.get("/", response_model=List[TaskOut])
def list_tasks(
    project_id: UUID | None = None,
    assignee_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Task)
    if project_id:
        q = q.filter(Task.project_id == project_id)
    if assignee_id:
        q = q.filter(Task.assignee_id == assignee_id)
    return q.order_by(Task.created_at.desc()).all()

@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        project_id=payload.project_id,
        name=payload.name,
        status=payload.status,
        assignee_id=payload.assignee_id,
        parent_id=payload.parent_id,
        asset_id=payload.asset_id,
        shot_id=payload.shot_id,
        due_at=payload.due_at,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
