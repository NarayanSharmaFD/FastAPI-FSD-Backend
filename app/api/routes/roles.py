"""
Role management API routes.
Provides endpoints for CRUD operations on roles.
Only accessible to admin users.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.role_service import RoleService
from app.schemas.role_schema import RoleCreate, RoleUpdate, RoleRead
from app.core.deps import get_current_user, require_admin
from app.models.models import User

router = APIRouter()


@router.post("/", response_model=RoleRead, dependencies=[Depends(require_admin)])
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role (admin only).
    
    Args:
        payload: Role creation data with permissions
        db: Database session
        
    Returns:
        RoleRead: Created role with permissions
    """
    service = RoleService(db)
    role = service.create_role(payload)
    
    # Convert to dict to ensure proper serialization
    role_dict = {
        "id": role.id,
        "role_name": role.role_name,
        "description": role.description,
        "permissions": role.permissions,
        "is_system_role": role.is_system_role,
        "created_at": role.created_at
    }
    return RoleRead(**role_dict)


@router.get("/", response_model=list[RoleRead])
def list_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all roles (accessible to all users).
    
    Args:
        skip: Number of records to skip
        limit: Maximum records to return
        db: Database session
        
    Returns:
        list[RoleRead]: List of roles
    """
    service = RoleService(db)
    roles = service.list_roles(skip=skip, limit=limit)
    
    # Convert to dict to ensure proper serialization
    result = []
    for role in roles:
        role_dict = {
            "id": role.id,
            "role_name": role.role_name,
            "description": role.description,
            "permissions": role.permissions,
            "is_system_role": role.is_system_role,
            "created_at": role.created_at
        }
        result.append(RoleRead(**role_dict))
    return result


@router.get("/{role_id}", response_model=RoleRead)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """
    Get role by ID (accessible to all users).
    
    Args:
        role_id: Role ID
        db: Database session
        
    Returns:
        RoleRead: Role with permissions
    """
    service = RoleService(db)
    role = service.get_role(role_id)
    
    # Convert to dict to ensure proper serialization
    role_dict = {
        "id": role.id,
        "role_name": role.role_name,
        "description": role.description,
        "permissions": role.permissions,
        "is_system_role": role.is_system_role,
        "created_at": role.created_at
    }
    return RoleRead(**role_dict)


@router.put("/{role_id}", response_model=RoleRead, dependencies=[Depends(require_admin)])
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a role (admin only).
    Cannot modify system roles or roles assigned to users.
    
    Args:
        role_id: Role ID
        payload: Update data
        db: Database session
        
    Returns:
        RoleRead: Updated role
    """
    service = RoleService(db)
    role = service.update_role(role_id, payload)
    
    # Convert to dict to ensure proper serialization
    role_dict = {
        "id": role.id,
        "role_name": role.role_name,
        "description": role.description,
        "permissions": role.permissions,
        "is_system_role": role.is_system_role,
        "created_at": role.created_at
    }
    return RoleRead(**role_dict)


@router.delete("/{role_id}", dependencies=[Depends(require_admin)])
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """
    Delete a role (admin only).
    Cannot delete system roles or roles assigned to users.
    
    Args:
        role_id: Role ID
        db: Database session
        
    Returns:
        dict: Confirmation message
    """
    service = RoleService(db)
    service.delete_role(role_id)
    return {"message": "Role deleted successfully"}


@router.get("/{role_id}/check-permission/{resource}/{action}")
def check_permission(
    role_id: int,
    resource: str,
    action: str,
    db: Session = Depends(get_db)
):
    """
    Check if a role has permission for an action on a resource.
    
    Args:
        role_id: Role ID
        resource: Resource type ('project' or 'task')
        action: Action type ('create', 'read', 'update', 'delete')
        db: Database session
        
    Returns:
        dict: Permission check result
    """
    if resource not in ["project", "task"]:
        raise HTTPException(
            status_code=400,
            detail="Resource must be 'project' or 'task'"
        )
    
    if action not in ["create", "read", "update", "delete"]:
        raise HTTPException(
            status_code=400,
            detail="Action must be 'create', 'read', 'update', or 'delete'"
        )
    
    service = RoleService(db)
    has_permission = service.check_permission(role_id, resource, action)
    
    return {
        "role_id": role_id,
        "resource": resource,
        "action": action,
        "has_permission": has_permission
    }
