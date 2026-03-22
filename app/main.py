from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models
from app.routers import notes, auth_router
from app.dependencies import get_current_user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth_router.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notiq API - By Devansh"}