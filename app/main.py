from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models
from app.routers import notes, auth_router
from app.dependencies import get_current_user
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.state.limiter = limiter #attaching limiter to app
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notiq API - By Devansh"}