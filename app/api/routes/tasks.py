from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Task, RoleEnum
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate
from app.core.deps import require_role, get_current_user

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    task = Task(**payload.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Task).offset(skip).limit(limit).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    data = payload.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return {"ok": True}
