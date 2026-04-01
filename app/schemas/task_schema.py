from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime, date
from app.models.models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[Union[datetime, date, str]] = None
    status: Optional[TaskStatus] = TaskStatus.not_started
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    assigned_user_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[Union[datetime, date, str]] = None
    status: Optional[TaskStatus] = None
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    assigned_user_id: Optional[int] = None
