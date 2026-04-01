from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from typing import Optional

from app.core.config import settings
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.models.models import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload or 'sub' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user_id = int(payload.get('sub'))
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(role: RoleEnum):
    def _require(user = Depends(get_current_user)):
        if user.role != role and user.role != RoleEnum.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return user
    return _require


def require_admin(user = Depends(get_current_user)):
    """
    Dependency to ensure user has admin role.
    Raises HTTP 403 if user is not admin.
    """
    if user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )
    return user

