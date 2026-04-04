from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate
import app.models as models
from app.auth import hash_password, verify_password, create_access_token
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request,user: UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(models.User).filter(models.User.email == user.email).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="email already registered")
  new_user = models.User(email=user.email, password = hash_password(user.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return {"message": "user registered successfully", "email":new_user.email}

@router.post("/login")
@limiter.limit("10/minute")
def login(request: Request,form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.email == form_data.username).first()
  if not user or not verify_password(form_data.password, user.password):
    raise HTTPException(status_code=402, detail="Invalid credentials")
  token = create_access_token({"user_id": user.id})
  return {"access_token":token, "token_type": "bearer"}

