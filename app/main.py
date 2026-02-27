from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models

# Creates tables in database automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

class NoteCreate(BaseModel):
    title: str
    content: str

@app.get("/")
def root():
    return {"message": "Welcome to Notiq API"}

@app.get("/notes")
def get_all_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return notes

@app.get("/notes/{id}")
def get_note(id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.post("/notes")
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/notes/{id}")
def update_note(id: int, note: NoteCreate, db: Session = Depends(get_db)):
    existing_note = db.query(models.Note).filter(models.Note.id == id).first()
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note not found")
    existing_note.title = note.title
    existing_note.content = note.content
    db.commit()
    db.refresh(existing_note)
    return existing_note

@app.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted successfully"}