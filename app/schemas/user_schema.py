from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = None  # Changed to string to support custom roles


class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None


class UserRead(UserBase):
    id: int
    role_id: Optional[int] = None
    permissions: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None  # Changed to string to support custom roles
    role_id: Optional[int] = None
    password: Optional[str] = None


class UserWithRole(UserRead):
    """Extended user response with role details"""
    role_name: Optional[str] = None
    role_description: Optional[str] = None
    role_permissions: Optional[Dict[str, Any]] = None

