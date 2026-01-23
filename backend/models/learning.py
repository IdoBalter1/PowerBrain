# backend/models/learning.py
from pydantic import BaseModel
from typing import Optional, List
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
    
    objective_id : Optional[str] = None
    status: Optional[str] = "pending"
    estimated_time_minutes: Optional[int] = None
    
    scheduled_date: Optional[datetime] = None
    start_time: Optional[str] = None  # ISO 8601 datetime string
    end_time: Optional[str] = None    # ISO 8601 datetime string
    calendar_event_id: Optional[str] = None
    
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    order: Optional[int] = None

class LearningPlanRequest(BaseModel):
    user_message: str
    maxdays:Optional[int] = 30

class LearningPlanResponse(BaseModel):
    objective: LearningObjective
    blocks: List[LearningBlock]
    calendar_events_created : Optional[int] = 0

