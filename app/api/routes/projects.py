from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db
from app.models.models import Project, RoleEnum
from app.schemas.project_schema import ProjectCreate, ProjectRead, ProjectUpdate
from app.core.deps import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev. Uncomment user=Depends(require_role(RoleEnum.task_creator)) to enable RBAC.
    try:
        from datetime import datetime
        
        # Get the create data
        create_data = payload.dict()
        
        # Convert date strings to datetime objects before creating ORM model
        for date_field in ['start_date', 'end_date']:
            if date_field in create_data and isinstance(create_data[date_field], str):
                try:
                    create_data[date_field] = datetime.fromisoformat(create_data[date_field])
                except (ValueError, TypeError):
                    create_data[date_field] = None
        
        project = Project(**create_data)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: projects.name" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint violation")
    except (ValueError, TypeError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format")


@router.get("/", response_model=list[ProjectRead])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Project).offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Not found")
        
        # Get the update data
        update_data = payload.dict(exclude_unset=True)
        
        # Convert date strings to datetime objects before setting on ORM model
        from datetime import datetime
        for date_field in ['start_date', 'end_date']:
            if date_field in update_data and isinstance(update_data[date_field], str):
                try:
                    update_data[date_field] = datetime.fromisoformat(update_data[date_field])
                except (ValueError, TypeError):
                    update_data[date_field] = None
        
        # Update the project
        for k, v in update_data.items():
            setattr(project, k, v)
        db.commit()
        db.refresh(project)
        return project
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: projects.name" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database constraint violation")
    except (ValueError, TypeError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data format")


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(project)
    db.commit()
    return {"ok": True}
