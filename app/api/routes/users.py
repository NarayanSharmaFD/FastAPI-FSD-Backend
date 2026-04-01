from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserRead, UserCreate, UserUpdate
from app.services.auth_service import AuthService
from app.core.deps import require_role, get_current_user
from app.models.models import RoleEnum, User

router = APIRouter()


def serialize_user(user: User) -> dict:
    """Convert User ORM object to dict for proper serialization.
    
    Returns the role name from the related Role object if available.
    Falls back to the legacy role enum field.
    Includes permissions from the user's role.
    """
    # Get role name: prefer role_obj.role_name, fallback to user.role
    if user.role_obj:
        role_name = user.role_obj.role_name
        permissions = user.role_obj.permissions
    else:
        role_name = user.role  # Use enum value as fallback
        permissions = None
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": role_name,  # Now can be any string (enum value or custom role name)
        "role_id": user.role_id,
        "permissions": permissions  # Include permissions from role
    }


@router.get("/me", response_model=UserRead)
def get_current_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current authenticated user information"""
    repo = UserRepository(db)
    user = repo.get_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserRead(**serialize_user(user))


@router.post("/", response_model=UserRead)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    svc = AuthService(db)
    existing = svc.users.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    user = svc.register_user(payload)
    
    # Serialize and return
    user_dict = serialize_user(user)
    return UserRead(**user_dict)


@router.get("/", response_model=list[UserRead])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    repo = UserRepository(db)
    users = repo.list(skip=skip, limit=limit)
    
    # Convert to dict to ensure proper serialization
    result = []
    for user in users:
        result.append(UserRead(**serialize_user(user)))
    return result


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserRead(**serialize_user(user))


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    repo.delete(user)
    return {"ok": True}


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    # NOTE: Auth disabled for local dev.
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.role is not None:
        user.role = payload.role
    if payload.role_id is not None:
        user.role_id = payload.role_id
    if payload.password:
        from app.core.security import get_password_hash
        user.hashed_password = get_password_hash(payload.password)
    repo.update()
    
    # Serialize and return
    user_dict = serialize_user(user)
    return UserRead(**user_dict)
