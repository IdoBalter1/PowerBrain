from fastapi import APIRouter, HTTPException, Depends
from models.learning import LearningObjective, LearningBlock, LearningPlanRequest, LearningPlanResponse
from core.models import objectives_db, blocks_db
from api.auth import get_current_user
import uuid
from typing import Optional
from datetime import datetime
from services.calendar_service import get_calendar_service, get_events
from services.ai_service import create_prompt,create_objective_from_request,create_events_from_ai_response
from services.ai_prompt import initial_prompt
import json
ai_router = APIRouter(prefix = "/ai", tags = ["ai"])

@ai_router.post("/create-learning-plan")
def create_learning_plan(learning_plan: LearningPlanRequest,username:str = Depends(get_current_user)):

    try: 
        user_prompt = learning_plan.user_message
        max_days = learning_plan.maxdays
        response = create_objective_from_request(initial_prompt.copy(),user_prompt,username,max_days = max_days)

        data = json.loads(response.choices[0].message.content)
        objective= LearningObjective(**data["objective"])
        blocks = [LearningBlock(**block) for block in data["blocks"]]
        created_events = create_events_from_ai_response(response)

        objective_id = str(uuid.uuid4())

        objective_dict = objective.dict()
        objective_dict["created_at"] = datetime.now()
        objective_dict["username"] = username

        objectives_db[objective_id] = objective_dict
        for block in blocks:
            block_id = str(uuid.uuid4())
            block_dict = block.dict()
            block_dict["objective_id"] = objective_id
            block_dict["created_at"] = datetime.now()
            block_dict["username"] = username
            blocks_db[block_id] = block_dict


        return LearningPlanResponse(
            objective=objective,
            blocks=blocks,
            calendar_events_created=len(created_events)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create learning plan: {str(e)}"
        )



