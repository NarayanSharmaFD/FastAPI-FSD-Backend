from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime, date

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[Union[datetime, date, str]] = None
    end_date: Optional[Union[datetime, date, str]] = None
    owner_id: Optional[int] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[Union[datetime, date, str]] = None
    end_date: Optional[Union[datetime, date, str]] = None
    owner_id: Optional[int] = None
