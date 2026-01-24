from fastapi import APIRouter, HTTPException, Depends
from api.auth import create_access_token, get_current_user, decode_JWT
from pydantic import BaseModel
from models.user import User,User_db, create_user
from db.database import get_db
from sqlalchemy.orm import Session


user_router = APIRouter(prefix = "/auth", tags=["auth"]) # continaer/grouping mechanism that groups realted endpoing together like a sub-app that gets merged into main app
class LoginRequest(BaseModel):
    username: str
    password: str


@user_router.post("/register")
async def register(user: User, db: Session = Depends(get_db)):

    db_user = db.query(User_db).filter(User_db.username == user.username).first()

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code = 409,
                detail="Username already exists"
            )
        else:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    access_token = create_access_token(data={"sub": user.username})

    create_user(db,user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "User registered successfully"
    }

@user_router.post("/login")
async def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(User_db).filter(User_db.username == user.username).first()
    if not db_user:
        raise HTTPException(
            status_code = 401,
            detail="Incorrect username or password" 
        )
    if not db_user.verify_password(user.password):
        raise HTTPException(
            status_code = 401,
            detail="Incorrect username or password"
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    else:
        access_token = create_access_token(data={"sub":user.username})
        return {"access_token": access_token, "token_type": "bearer"}
