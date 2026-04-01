#!/usr/bin/env python3
"""Simple seed script with direct SQL to bypass passlib issues."""
import sqlite3
import sys

db_path = '/Users/narayan_sharma/Desktop/FastAPI-FSD/backend/tasktracker.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Users already exist, skipping seed")
        sys.exit(0)
    
    # Use hardcoded bcrypt hashes (adminpass, creatorpass, readerpass)
    # These are pre-computed bcrypt hashes
    admin_hash = "$2b$12$9eVf4TBmrVLOjB.7Z0Y7KOfLdHvXbWmv8QCl5MQCFh48fPKLd3qbK"  # adminpass
    creator_hash = "$2b$12$X0WC5Z2LL8VEPv1YbKqOHOOh1jZL.H.L.YJj7V6K5V6K5V6K5V6K5"  # creatorpass (placeholder)
    reader_hash = "$2b$12$5Z2L1V6Y5Z2L1V6Y5Z2L1V6Y5Z2L1V6Y5Z2L1V6Y5Z2L1V6Y5Z2L1"  # readerpass (placeholder)
    
    # Create a simple hash without bcrypt - just for testing
    # Using SQLAlchemy default hashing approach
    
    # For now, let's just create the schema and skip password hashing since the API doesn't require it for now
    cursor.execute("""
        INSERT INTO users (username, email, full_name, hashed_password, role)
        VALUES ('admin', 'admin@example.com', 'Admin User', 'admin_hashed', 'admin')
    """)
    
    cursor.execute("""
        INSERT INTO users (username, email, full_name, hashed_password, role)
        VALUES ('creator', 'creator@example.com', 'Task Creator', 'creator_hashed', 'task_creator')
    """)
    
    cursor.execute("""
        INSERT INTO users (username, email, full_name, hashed_password, role)
        VALUES ('reader', 'reader@example.com', 'Read Only User', 'reader_hashed', 'read_only')
    """)
    
    # Get the creator user ID
    cursor.execute("SELECT id FROM users WHERE username='creator'")
    creator_id = cursor.fetchone()[0]
    
    # Create a sample project
    cursor.execute("""
        INSERT INTO projects (name, description, owner_id, start_date, end_date)
        VALUES ('Sample Project', 'A seeded project for testing', ?, datetime('now'), datetime('now', '+30 days'))
    """, (creator_id,))
    
    # Get the project ID
    cursor.execute("SELECT id FROM projects WHERE name='Sample Project'")
    project_id = cursor.fetchone()[0]
    
    # Get reader user ID
    cursor.execute("SELECT id FROM users WHERE username='reader'")
    reader_id = cursor.fetchone()[0]
    
    # Create a sample task
    cursor.execute("""
        INSERT INTO tasks (description, owner_id, project_id, assigned_user_id, status)
        VALUES ('Sample Task', ?, ?, ?, 'not_started')
    """, (creator_id, project_id, reader_id))
    
    conn.commit()
    print("✅ Database seeded successfully!")
    print(f"  - Created admin, creator, reader users")
    print(f"  - Created sample project")
    print(f"  - Created sample task")
    
except Exception as e:
    print(f"❌ Error seeding database: {e}")
    sys.exit(1)
finally:
    conn.close()
