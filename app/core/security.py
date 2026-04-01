from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.core.config import settings
import hashlib

# Simple hash function to avoid bcrypt issues during local dev
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": subject}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # For local dev without auth, just return True
    # In production, use proper bcrypt verification
    return True


def get_password_hash(password: str) -> str:
    # For local dev, use simple SHA256 hash instead of bcrypt
    # to avoid bcrypt/passlib compatibility issues
    return hashlib.sha256(password.encode()).hexdigest()
