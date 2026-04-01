"""
Role schema for role management API.
Defines Pydantic models for role CRUD operations.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class PermissionBase(BaseModel):
    """Base permission structure"""
    create: bool = False
    read: bool = True
    update: bool = False
    delete: bool = False


class PermissionsSchema(BaseModel):
    """Permissions schema with project and task permissions"""
    project: PermissionBase = Field(default_factory=lambda: PermissionBase())
    task: PermissionBase = Field(default_factory=lambda: PermissionBase())


class RoleCreate(BaseModel):
    """Schema for creating a new role"""
    role_name: str = Field(..., min_length=1, max_length=80)
    description: Optional[str] = Field(None, max_length=500)
    permissions: PermissionsSchema


class RoleUpdate(BaseModel):
    """Schema for updating a role"""
    role_name: Optional[str] = Field(None, min_length=1, max_length=80)
    description: Optional[str] = Field(None, max_length=500)
    permissions: Optional[PermissionsSchema] = None


class RoleRead(BaseModel):
    """Schema for reading role data"""
    id: int
    role_name: str
    description: Optional[str]
    permissions: Dict[str, Any]
    is_system_role: int
    created_at: datetime

    class Config:
        from_attributes = True


class RoleWithUserCount(RoleRead):
    """Role with count of assigned users"""
    user_count: int = 0
