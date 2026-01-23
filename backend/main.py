import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from api.auth import get_current_user, create_access_token
from core.models import users_db
from typing import List
from core.config import settings
from api.routes import user_router
from api.objectives import objectives_router
from api.calendar import calendar_router
from api.ai import ai_router



app = FastAPI(
    title="Up your learning",
    desdcription="this is where you organise your learning",
    version="0.1.0",
    docs_url = "/docs",
    redoc__url="/redoc"

) 


origins = [
    "http://localhost:3000","http://localhost:5371" # base origin of anything that we want to call anything on our server
]

# allow certain origins to interact with our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_credentials = True, 
    allow_methods=["*"], #GET (retrieve data) POST ( making data ) PUT (updating data)
    allow_headers=["*"], # additional information you send with requests
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

app.include_router(user_router)
app.include_router(objectives_router) 
app.include_router(calendar_router)
app.include_router(ai_router)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
