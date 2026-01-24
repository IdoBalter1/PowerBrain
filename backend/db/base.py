from db.database import Base

# Import all models here so Alembic can detect them
from models.user import User_db  # Import the SQLAlchemy model, not Pydantic

__all__ = ["Base", "User_db"]