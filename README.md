# FastAPI Task Tracker (Backend)

This backend is a FastAPI application structured with Clean Architecture principles.

Requirements:
- Python 3.11+
- Docker (for Postgres)

Quickstart (local):
1. Copy `.env.example` to `.env` and set values.
2. Start Postgres: `docker-compose up -d` (from backend/)
3. Create a virtualenv and install requirements: `pip install -r requirements.txt`
4. Run Alembic migrations (optional) or let the app create tables on startup.
5. Seed sample data: `python -m scripts.seed`
6. Run: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

API docs available at `http://localhost:8000/docs`.

Production notes and Azure deployment instructions are in the root README.
