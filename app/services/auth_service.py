from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.user_schema import UserCreate
from app.models.models import User
from datetime import timedelta
from app.core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> User:
        user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            role=user_in.role or "read_only",
            role_id=user_in.role_id,
        )
        return self.users.create(user)

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.users.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token_for_user(self, user: User):
        return create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
