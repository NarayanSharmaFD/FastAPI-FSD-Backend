from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime, date

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[Union[datetime, date, str]] = None
    end_date: Optional[Union[datetime, date, str]] = None
    owner_id: Optional[int] = None
    
    @field_validator('start_date', 'end_date', mode='before')
    @classmethod
    def parse_dates(cls, v):
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

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[Union[datetime, date, str]] = None
    end_date: Optional[Union[datetime, date, str]] = None
    owner_id: Optional[int] = None
