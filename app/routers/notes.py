from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NoteCreate
import app.models as models
from app.dependencies import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("")
def get_all_notes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  notes = db.query(models.Note).filter(models.Note.user_id == current_user.id).all()
  return notes

@router.get("/{id}")
def get_note(id:int,db:Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
  if not note:
    raise HTTPException(status_code=404, detail="note not found")
  return note

@router.post("")
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  new_note=models.Note(title=note.title, content = note.content, user_id = current_user.id)
  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@router.put("/{id}")
def update_note(id:int, note: NoteCreate, db:Session = Depends(get_db), current_user : models.User = Depends(get_current_user)):
  existing_note = db.query(models.Note). filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
  if not existing_note:
    raise HTTPException(status_code=404, detail="note not found")
  existing_note.title = note.title
  existing_note.content = note.content
  db.commit()
  db.refresh(existing_note)
  return existing_note

@router.delete("/{id}")
def delete_note(id:int, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id).first()
  if not note:
    raise HTTPException(status_code=404, detail="note not found")
  db.delete(note)
  db.commit()
  return {"message": "Note deleted successfully"}


  
