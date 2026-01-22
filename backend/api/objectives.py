from fastapi import APIRouter, HTTPException
from backend.models.learning import LearningObjective, LearningBlock

from pydantic import BaseModel
from backend.core.models import users_db


objectives_router = APIRouter(prefix = "/objectives", tags=["auth"])

@objectives_router.post("/objectives")
async def create_objective(objective:LearningObjective):
    pass


@objectives_router.post(f"/objectives/{id}/blocks")
async def create_block(objective_block:LearningBlock):
    pass

@objectives_router.get("/objectives")
async def get_objective(objective:LearningObjective):
    pass


@objectives_router.get(f"/objectives/{id}/blocks")
async def get_block(objective_block:LearningBlock):
    pass
