from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate, UserRead
from app.schemas.token_schema import Token
from app.core.deps import get_current_user
from app.models.models import User
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict, Any

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    svc = AuthService(db)
    existing = svc.users.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user = svc.register_user(payload)
    return user

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    svc = AuthService(db)
    user = svc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = svc.create_access_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/permissions", response_model=Dict[str, Any])
def get_user_permissions(current_user: User = Depends(get_current_user)):
    """Get permissions for the currently authenticated user based on their role"""
    if current_user.role_obj and current_user.role_obj.permissions:
        return {
            "permissions": current_user.role_obj.permissions,
            "role": current_user.role_obj.role_name
        }
    # Return default minimal permissions if no role assigned
    return {
        "permissions": {
            "project": {"create": False, "read": True, "update": False, "delete": False},
            "task": {"create": False, "read": True, "update": False, "delete": False}
        },
        "role": current_user.role or "read_only"
    }
