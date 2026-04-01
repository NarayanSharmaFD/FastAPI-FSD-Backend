from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base


class RoleEnum(str, enum.Enum):
    admin = "admin"
    task_creator = "task_creator"
    read_only = "read_only"


class Role(Base):
    """
    Role model for managing permissions and access control.
    Permissions are stored as JSON with structure:
    {
      "project": {"create": bool, "read": bool, "update": bool, "delete": bool},
      "task": {"create": bool, "read": bool, "update": bool, "delete": bool}
    }
    """
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(80), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    permissions = Column(JSON, nullable=False, default={
        "project": {"create": False, "read": True, "update": False, "delete": False},
        "task": {"create": False, "read": True, "update": False, "delete": False}
    })
    is_system_role = Column(Integer, default=0)  # 0=custom, 1=system (cannot delete)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="role_obj")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=True)
    hashed_password = Column(String(256), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    # Legacy role column - now stores role name (string) instead of enum
    # This allows support for custom roles
    role = Column(String(80), default="read_only")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    role_obj = relationship("Role", back_populates="users")
    projects = relationship("Project", back_populates="owner_obj", foreign_keys="Project.owner_id")
    owned_tasks = relationship("Task", back_populates="owner_obj", foreign_keys="Task.owner_id")
    assigned_tasks = relationship("Task", back_populates="assigned_user_obj", foreign_keys="Task.assigned_user_id")

    @property
    def role_permissions(self):
        """Get permissions from related role"""
        if self.role_obj:
            return self.role_obj.permissions
        return None


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner_obj = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project_obj", cascade="all, delete-orphan")


class TaskStatus(str, enum.Enum):
    new = "new"
    in_progress = "in-progress"
    blocked = "blocked"
    completed = "completed"
    not_started = "not started"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.not_started)
    owner_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

    owner_obj = relationship("User", foreign_keys=[owner_id], back_populates="owned_tasks")
    assigned_user_obj = relationship("User", foreign_keys=[assigned_user_id], back_populates="assigned_tasks")
    project_obj = relationship("Project", back_populates="tasks")
