from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.models.models import Task, RoleEnum
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate
from app.core.deps import require_role, get_current_user

router = APIRouter()


@router.post("/", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    try:
        task = Task(**payload.dict())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint violation")
    except (ValueError, TypeError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format")


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
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Not found")
        
        # Get the update data
        update_data = payload.dict(exclude_unset=True)
        
        # Convert date strings to datetime objects before setting on ORM model
        from datetime import datetime
        if 'due_date' in update_data and isinstance(update_data['due_date'], str):
            try:
                update_data['due_date'] = datetime.fromisoformat(update_data['due_date'])
            except (ValueError, TypeError):
                update_data['due_date'] = None
        
        # Update the task
        for k, v in update_data.items():
            setattr(task, k, v)
        db.commit()
        db.refresh(task)
        return task
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint violation")
    except (ValueError, TypeError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format")


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return {"ok": True}
