from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(BaseModel):
    username: str
    password: str
    email: str
    google_calendar_link: Optional[str] = None