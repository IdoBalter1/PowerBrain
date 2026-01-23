from fastapi import APIRouter, HTTPException, Depends
from models.learning import LearningObjective, LearningBlock
from core.models import objectives_db, blocks_db
from api.auth import get_current_user
import uuid
from typing import Optional
from datetime import datetime
from services.calendar_service import get_calendar_service, get_events
from services.ai_service import create_events_from_ai_response

calendar_router = APIRouter(prefix = "/calendar", tags = ["calendar"])

@calendar_router.get("/events")
async def get_calendar_events(maxdays : Optional[int] = 30, username: str = Depends(get_current_user)):

    try:
        events = get_events(maxdays=maxdays)
        
        if not events:
            return {"events": []}
        
        # Format events for frontend calendar
        formatted_events = []
        for event in events:
            start = event.get("start", {})
            end = event.get("end", {})
            
            formatted_events.append({
                "id": event.get("id"),
                "title": event.get("summary", "No title"),
                "start": start.get("dateTime") or start.get("date"),
                "end": end.get("dateTime") or end.get("date"),
                "description": event.get("description", ""),
                "location": event.get("location", ""),
                "htmlLink": event.get("htmlLink", ""),
                "isLearning": "Learning:" in event.get("summary", "")
            })
        
        return {"events": formatted_events}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch calendar events: {str(e)}"
        )

