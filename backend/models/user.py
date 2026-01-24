from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
from db.database import Base
import bcrypt
from sqlalchemy.orm import Session
class User(BaseModel):
    username: str
    password: str
    email: str
    google_calendar_link: Optional[str] = None

class User_db(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    google_calendar_link = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def verify_password(self, password: str) -> bool:
        # Ensure password is bytes for bcrypt
        if isinstance(password, str):
            password = password.encode('utf-8')
        # Ensure hashed_password is bytes
        if isinstance(self.hashed_password, str):
            hashed_password = self.hashed_password.encode('utf-8')
        else:
            hashed_password = self.hashed_password
        return bcrypt.checkpw(password, hashed_password)
    
    @staticmethod
    def hash_password(password: str) -> str:
        # Ensure password is a string
        if isinstance(password, bytes):
            password = password.decode('utf-8', errors='ignore')
        elif not isinstance(password, str):
            password = str(password)
    
        password = password.strip()
        password_bytes = password.encode('utf-8')
        # Bcrypt limitation: passwords must be <= 72 bytes
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]

        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed.decode('utf-8')

def create_user(db: Session, user: User):
    try:
        # Hash the password
        hashed_password = User_db.hash_password(user.password)
        
        # Create the database model instance
        db_item = User_db(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            google_calendar_link=user.google_calendar_link
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise



