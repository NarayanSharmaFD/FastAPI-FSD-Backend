#!/usr/bin/env python3
"""
Seed script to populate the database with demo users.
Run this script to create demo credentials for testing.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.models.models import User, RoleEnum
from app.core.security import get_password_hash
from app.db.base import Base

def seed_users():
    """Create demo users for testing"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("✓ Users already exist in database")
            return
        
        # Demo users to create
        demo_users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "full_name": "Administrator",
                "password": "password",
                "role": RoleEnum.admin
            },
            {
                "username": "creator",
                "email": "creator@example.com",
                "full_name": "Task Creator",
                "password": "password",
                "role": RoleEnum.task_creator
            },
            {
                "username": "viewer",
                "email": "viewer@example.com",
                "full_name": "Read Only User",
                "password": "password",
                "role": RoleEnum.read_only
            },
        ]
        
        # Create users
        for user_data in demo_users:
            password = user_data.pop("password")
            user = User(
                **user_data,
                hashed_password=get_password_hash(password)
            )
            db.add(user)
            print(f"✓ Created user: {user_data['username']} (role: {user_data['role']})")
        
        db.commit()
        print("\n✅ Database seeded successfully!")
        print("\nDemo Credentials:")
        print("─" * 40)
        print("Admin:   admin / password")
        print("Creator: creator / password")
        print("Viewer:  viewer / password")
        print("─" * 40)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()
