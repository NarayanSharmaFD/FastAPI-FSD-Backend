from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Project, RoleEnum
from app.schemas.project_schema import ProjectCreate, ProjectRead, ProjectUpdate
from app.core.deps import get_current_user, require_role

router = APIRouter()


@router.post("/", response_model=ProjectRead)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev. Uncomment user=Depends(require_role(RoleEnum.task_creator)) to enable RBAC.
    project = Project(**payload.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


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
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(project, k, v)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(project)
    db.commit()
    return {"ok": True}
