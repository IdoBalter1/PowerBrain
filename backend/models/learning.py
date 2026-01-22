# backend/models/learning.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LearningObjective(BaseModel):
    title: str # what you're learning
    content: str

    tags : Optional[List[str]] = []
    difficulty: Optional[str] = None  # "easy", "medium", "hard"
    estimated_time_hours: Optional[int] = None
    target_completion_date: Optional[datetime] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Optional[str] = "in_progress"
    


class LearningBlock(BaseModel):
    title: str
    subtitle: Optional[str] = None
    
    objective_id : Optional[str] = None # A learning Block bleongs to a LearningObjective
    status: Optional[str] = "pending"  # pending, in_progress, completed
    estimated_time_minutes: Optional[int] = None
    
    # Calendar
    scheduled_date: Optional[datetime] = None
    calendar_event_id: Optional[str] = None
    
    # Metadata
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    order: Optional[int] = None  # Sequence order

