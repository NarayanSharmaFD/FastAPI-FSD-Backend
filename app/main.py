from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
# Import models to register them with Base
from app.models.models import User, Project, Task, Role  # noqa: F401
from app.api.routes import auth, users, projects, tasks, roles
from app.core.logging_config import setup_logging

setup_logging()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

    # Create DB tables (Alembic preferred for production)
    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o for o in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"]) 
    app.include_router(roles.router, prefix="/api/roles", tags=["roles"]) 
    app.include_router(users.router, prefix="/api/users", tags=["users"]) 
    app.include_router(projects.router, prefix="/api/projects", tags=["projects"]) 
    app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"]) 

    return app

app = create_app()
