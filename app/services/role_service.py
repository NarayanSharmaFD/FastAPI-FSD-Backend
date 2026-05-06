"""
Role service for business logic operations.
Handles role management, permissions, and validation.
"""
from sqlalchemy.orm import Session
from app.repositories.role_repository import RoleRepository
from app.schemas.role_schema import RoleCreate, RoleUpdate, RoleRead
from fastapi import HTTPException


class RoleService:
    """Service for role management operations"""
    
    def __init__(self, db: Session):
        """Initialize service with database session"""
        self.db = db
        self.repository = RoleRepository(db)
    
    def create_role(self, role_data: RoleCreate) -> RoleRead:
        """
        Create a new role with permissions.
        
        Args:
            role_data: Role creation payload
            
        Returns:
            RoleRead: Created role
            
        Raises:
            HTTPException: If role name already exists
        """
        # Check if role already exists
        existing = self.repository.get_by_name(role_data.role_name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Role '{role_data.role_name}' already exists"
            )
        
        # Convert permissions to dict
        permissions = {
            "project": role_data.permissions.project.dict(),
            "task": role_data.permissions.task.dict()
        }
        
        role_dict = {
            "role_name": role_data.role_name,
            "description": role_data.description,
            "permissions": permissions,
            "is_system_role": 0
        }
        
        return self.repository.create(role_dict)
    
    def get_role(self, role_id: int) -> RoleRead:
        """
        Get role by ID.
        
        Args:
            role_id: Role ID
            
        Returns:
            RoleRead: Role data
            
        Raises:
            HTTPException: If role not found
        """
        role = self.repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    
    def list_roles(self, skip: int = 0, limit: int = 100) -> list[RoleRead]:
        """
        List all roles with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            list[RoleRead]: List of roles
        """
        return self.repository.list(skip=skip, limit=limit)
    
    def update_role(self, role_id: int, role_data: RoleUpdate) -> RoleRead:
        """
        Update a role.
        
        Args:
            role_id: Role ID
            role_data: Update payload
            
        Returns:
            RoleRead: Updated role
            
        Raises:
            HTTPException: If role not found or is system role
        """
        role = self.repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        if role.is_system_role:
            raise HTTPException(
                status_code=403,
                detail="Cannot modify system roles"
            )
        
        # Update fields
        if role_data.role_name is not None:
            # Check if new name conflicts
            existing = self.repository.get_by_name(role_data.role_name)
            if existing and existing.id != role_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Role '{role_data.role_name}' already exists"
                )
            role.role_name = role_data.role_name
        
        if role_data.description is not None:
            role.description = role_data.description
        
        if role_data.permissions is not None:
            role.permissions = {
                "project": role_data.permissions.project.dict(),
                "task": role_data.permissions.task.dict()
            }
        
        return self.repository.update(role)
    
    def delete_role(self, role_id: int) -> bool:
        
        role = self.repository.get_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        if role.is_system_role:
            raise HTTPException(
                status_code=403,
                detail="Cannot delete system roles"
            )
        
        # Check if role is assigned to users
        if role.users:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete role assigned to {len(role.users)} user(s)"
            )
        
        return self.repository.delete(role)
    
    def check_permission(self, role_id: int, resource: str, action: str) -> bool:
        
        role = self.repository.get_by_id(role_id)
        if not role:
            return False
        
        permissions = role.permissions
        if resource not in permissions:
            return False
        
        return permissions[resource].get(action, False)
