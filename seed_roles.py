#!/usr/bin/env python3
"""
Seed script to populate database with initial roles and users.
Creates system roles with appropriate permissions.
"""
import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models.models import Role, User, Base, RoleEnum
from app.core.security import get_password_hash

def seed_roles(db: Session):
    """Seed initial roles with permissions"""
    
    roles_data = [
        {
            "role_name": "admin",
            "description": "Full system access with all permissions",
            "permissions": {
                "project": {"create": True, "read": True, "update": True, "delete": True},
                "task": {"create": True, "read": True, "update": True, "delete": True}
            },
            "is_system_role": 1
        },
        {
            "role_name": "task_creator",
            "description": "Can create and manage tasks, limited project access",
            "permissions": {
                "project": {"create": False, "read": True, "update": False, "delete": False},
                "task": {"create": True, "read": True, "update": True, "delete": False}
            },
            "is_system_role": 1
        },
        {
            "role_name": "read_only",
            "description": "Read-only access, can mark tasks as complete",
            "permissions": {
                "project": {"create": False, "read": True, "update": False, "delete": False},
                "task": {"create": False, "read": True, "update": False, "delete": False}
            },
            "is_system_role": 1
        }
    ]
    
    for role_data in roles_data:
        # Check if role exists
        existing = db.query(Role).filter(Role.role_name == role_data["role_name"]).first()
        if existing:
            print(f"✓ Role '{role_data['role_name']}' already exists")
            continue
        
        role = Role(**role_data)
        db.add(role)
        print(f"+ Created role: {role_data['role_name']}")
    
    db.commit()
    print("✓ Roles seeded successfully\n")


def seed_users(db: Session):
    """Seed initial users with roles"""
    
    users_data = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "full_name": "Admin User",
            "password": "password",
            "role": RoleEnum.admin,
            "role_id": 1
        },
        {
            "username": "creator",
            "email": "creator@example.com",
            "full_name": "Task Creator",
            "password": "password",
            "role": RoleEnum.task_creator,
            "role_id": 2
        },
        {
            "username": "viewer",
            "email": "viewer@example.com",
            "full_name": "Viewer User",
            "password": "password",
            "role": RoleEnum.read_only,
            "role_id": 3
        }
    ]
    
    for user_data in users_data:
        # Check if user exists
        existing = db.query(User).filter(User.username == user_data["username"]).first()
        if existing:
            print(f"✓ User '{user_data['username']}' already exists")
            continue
        
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            hashed_password=get_password_hash(user_data["password"]),
            role=user_data["role"],
            role_id=user_data.get("role_id")
        )
        db.add(user)
        print(f"+ Created user: {user_data['username']} ({user_data['full_name']})")
    
    db.commit()
    print("✓ Users seeded successfully\n")


def main():
    """Main seed function"""
    print("\n" + "="*60)
    print("Task Tracker Database Seeding")
    print("="*60 + "\n")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created\n")
    
    # Get session
    db = SessionLocal()
    
    try:
        # Seed roles
        print("Seeding roles...")
        seed_roles(db)
        
        # Seed users
        print("Seeding users...")
        seed_users(db)
        
        print("="*60)
        print("✓ Seeding completed successfully!")
        print("="*60)
        print("\nDemo Credentials:")
        print("-" * 60)
        print("Admin:       admin / password")
        print("Creator:     creator / password")
        print("Viewer:      viewer / password")
        print("-" * 60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Seeding failed: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
