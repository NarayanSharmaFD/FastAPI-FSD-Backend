"""
Role repository for data access operations.
Follows repository pattern for separation of concerns.
"""
from sqlalchemy.orm import Session
from app.models.models import Role


class RoleRepository:
    """Repository for Role entity operations"""
    
    def __init__(self, db: Session):
        """Initialize repository with database session"""
        self.db = db
    
    def get_by_id(self, role_id: int) -> Role:
        """Get role by ID"""
        return self.db.query(Role).filter(Role.id == role_id).first()
    
    def get_by_name(self, role_name: str) -> Role:
        """Get role by name"""
        return self.db.query(Role).filter(Role.role_name == role_name).first()
    
    def list(self, skip: int = 0, limit: int = 100) -> list[Role]:
        """List all roles with pagination"""
        return self.db.query(Role).offset(skip).limit(limit).all()
    
    def create(self, role_data: dict) -> Role:
        """Create a new role"""
        db_role = Role(**role_data)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role
    
    def update(self, role: Role) -> Role:
        """Update an existing role"""
        self.db.commit()
        self.db.refresh(role)
        return role
    
    def delete(self, role: Role) -> bool:
        """Delete a role (prevent deletion of system roles)"""
        if role.is_system_role:
            raise ValueError("Cannot delete system roles")
        self.db.delete(role)
        self.db.commit()
        return True
    
    def get_user_count(self, role_id: int) -> int:
        """Get number of users assigned to this role"""
        return self.db.query(Role).filter(Role.id == role_id).first().users.__len__() if self.get_by_id(role_id) else 0
