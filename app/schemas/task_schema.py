from pydantic import BaseModel, field_validator
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
    
    @field_validator('due_date', mode='before')
    @classmethod
    def parse_due_date(cls, v):
        if v is None:
            return None
        if isinstance(v, (datetime, date)):
            return v
        if isinstance(v, str):
            # Try parsing ISO format
            try:
                return datetime.fromisoformat(v)
            except (ValueError, TypeError):
                return None
        return v

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[Union[datetime, date, str]] = None
    status: Optional[TaskStatus] = None
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    assigned_user_id: Optional[int] = None
