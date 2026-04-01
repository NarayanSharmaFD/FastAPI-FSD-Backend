"""Seed script to create sample users, roles, projects and tasks."""
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.models import User, Project, Task


def seed():
    db: Session = SessionLocal()
    try:
        # create sample users
        admin = User(username='admin', email='admin@example.com', full_name='Admin User', hashed_password=get_password_hash('adminpass'), role='admin')
        creator = User(username='creator', email='creator@example.com', full_name='Task Creator', hashed_password=get_password_hash('creatorpass'), role='task_creator')
        reader = User(username='reader', email='reader@example.com', full_name='Read Only', hashed_password=get_password_hash('readerpass'), role='read_only')
        db.add_all([admin, creator, reader])
        db.commit()

        project = Project(name='Sample Project', description='Seeded project', owner_id=creator.id)
        db.add(project)
        db.commit()

        task = Task(description='Sample Task', owner_id=creator.id, project_id=project.id, assigned_user_id=reader.id)
        db.add(task)
        db.commit()

        print('Seeded data')
    finally:
        db.close()

if __name__ == '__main__':
    seed()
