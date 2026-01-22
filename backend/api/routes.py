from fastapi import APIRouter, HTTPException
from models.user import User
from api.auth import create_access_token, get_current_user, decode_JWT
from pydantic import BaseModel
from core.models import users_db


user_router = APIRouter(prefix = "/auth", tags=["auth"]) # continaer/grouping mechanism that groups realted endpoing together like a sub-app that gets merged into main app
class LoginRequest(BaseModel):
    username: str
    password: str


@user_router.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(
            status_code = 409,
            detail="Username already exists"
        )
    users_db[user.username] = user

    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "User registered successfully"
    }

@user_router.post("/login")
async def login(user: LoginRequest):
    if user.username not in users_db:
        raise HTTPException(
            status_code = 401,
            detail="Incorrect username or password" 
        )
    if users_db[user.username].password != user.password:
        raise HTTPException(
            status_code = 401,
            detail="Incorrect username or password"
        )
    else:
        access_token = create_access_token(data={"sub":user.username})
        return {"access_token": access_token, "token_type": "bearer"}
