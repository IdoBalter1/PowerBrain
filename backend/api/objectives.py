from fastapi import APIRouter, HTTPException, Depends
from backend.models.learning import LearningObjective, LearningBlock
from backend.core.models import objectives_db, blocks_db
from api.auth import get_current_user
import uuid
from datetime import datetime



objectives_router = APIRouter(prefix = "/objectives", tags=["objectives"])


@objectives_router.post("")
async def create_objective(objective:LearningObjective, username:str = Depends(get_current_user)):
    # recieve objective data from AI/frontend
    # store it
    # return success
    objective_id = str(uuid.uuid4())

    objective_dict = objective.dict()
    objective_dict["created_at"] = datetime.now()
    objective_dict["username"] = username

    objectives_db[objective_id] = objective_dict

    return{
        "id": objective_id,
        "objective": objective_dict,
        "message": "Created Objective Successfully"
    }


@objectives_router.post("/{objective_id}/blocks")
async def create_block(objective_id:str, block:LearningBlock, username:str = Depends(get_current_user)):

    if objective_id not in objectives_db:
        raise HTTPException(404, "Objective not found")
    if objectives_db[objective_id].get("username") != username:
        raise HTTPException(status_code=403, detail="Not authorized")
    block_id = str(uuid.uuid4())


    block_dict = block.dict()
    block_dict["objective_id"] = objective_id
    block_dict["created_at"] = datetime.now()
    block_dict["username"] = username
    blocks_db[block_id] = block_dict

    return{
        "id": block_id,
        "block": block_dict,
        "message": "Created Block Successfully"
    }

@objectives_router.get("")
async def get_all_objective(username: str = Depends(get_current_user)):
    return {
        "objectives" :[{
            "id" : id, **obj}
            for id,obj in objectives_db.items()
            if obj.get("username") == username
        ]
    }


@objectives_router.get("/{objective_id}/blocks")
async def get_blocks(objective_id:str, username : str = Depends(get_current_user)):
    if objective_id not in objectives_db:
        raise HTTPException(status_code=404, detail="Objective not found")
    
    if objectives_db[objective_id].get("username") != username:
        raise HTTPException(status_code=403, detail="Not authorized")
    blocks = [
        {"id": id, **block}
        for id,block in blocks_db.items() if block.get("objective_id") == objective_id
    ]
    return {"blocks": blocks}
