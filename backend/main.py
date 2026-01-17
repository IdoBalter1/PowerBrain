import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from api.auth import get_current_user, create_access_token
from database.models import users_db
from typing import List




app = FastAPI()


origins = [
    "http://localhost:3000" # base origin of anything that we want to call anything on our server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_creditinals = True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

memory_db = {}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! This is a protected resource."}