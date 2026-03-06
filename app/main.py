from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models
from app.auth import hash_password, verify_password, create_access_token, verify_access_token

Base.metadata.create_all(bind=engine)
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class NoteCreate(BaseModel):
    title: str
    content: str

class UserCreate(BaseModel):
    email: str
    password: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@app.get("/")
def root():
    return {"message": "Welcome to Notiq API"}

@app.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(email=user.email, password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "email": new_user.email}

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/notes")
def get_all_notes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    notes = db.query(models.Note).filter(models.Note.user_id == current_user.id).all()
    return notes

@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_note = models.Note(title=note.title, content=note.content, user_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{id}")
def update_note(id: int, note: NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing_note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note.title = note.title
    existing_note.content = note.content
    db.commit()
    db.refresh(existing_note)
    return existing_note

@app.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}