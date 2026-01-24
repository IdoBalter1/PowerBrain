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
    try:
        existing_user = db.query(User_db).filter(User_db.username == user.username).first()

        if existing_user:
            if existing_user.username == user.username:
                raise HTTPException(
                    status_code=409,
                    detail="Username already exists"
                )
            else:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )

        # Create user in database
        db_user = create_user(db, user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "message": "User registered successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        # Handle database integrity errors (race conditions)
        if "UNIQUE constraint" in str(e) or "IntegrityError" in str(type(e).__name__):
            if "email" in str(e).lower():
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists"
                )
            elif "username" in str(e).lower():
                raise HTTPException(
                    status_code=409,
                    detail="Username already exists"
                )
        print(f"Error in register: {e}") 
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


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
