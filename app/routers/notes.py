from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.database import get_db
from app.schemas import NoteCreate
import app.models as models
from app.dependencies import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/notes", tags=["Notes"])

def cleanup_expired_notes(db: Session, user_id= int):
  thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
  db.query(models.Note).filter(
    models.Note.user_id == user_id,
    models.Note.deleted_at != None,
    models.Note.deleted_at < thirty_days_ago
  ).delete()
  db.commit()

@router.get("")
@limiter.limit("60/minute")
def get_all_notes(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  cleanup_expired_notes(db, current_user.id)
  notes = db.query(models.Note).filter(models.Note.user_id == current_user.id, models.Note.deleted_at == None).all()
  return notes

@router.get("/trash")
@limiter.limit("60/minute")
def get_trash(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  cleanup_expired_notes(db, current_user.id)
  notes = db.query(models.Note). filter(
    models.Note.user_id == current_user.id,
    models.Note.deleted_at != None
  ).all()
  return notes

@router.get("/{id}")
@limiter.limit("60/minute")
def get_note(request: Request,id:int,db:Session=Depends(get_db), current_user: models.User = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id, models.Note.deleted_at==None).first()
  if not note:
    raise HTTPException(status_code=404, detail="note not found")
  return note

@router.post("")
@limiter.limit("30/minute")
def create_note(request: Request,note: NoteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  new_note=models.Note(title=note.title, content = note.content, user_id = current_user.id)
  db.add(new_note)
  db.commit()
  db.refresh(new_note)
  return new_note

@router.put("/{id}")
@limiter.limit("30/minute")
def update_note(request: Request,id:int, note: NoteCreate, db:Session = Depends(get_db), current_user : models.User = Depends(get_current_user)):
  existing_note = db.query(models.Note). filter(models.Note.id == id, models.Note.user_id == current_user.id, models.Note.deleted_at == None).first()
  if not existing_note:
    raise HTTPException(status_code=404, detail="note not found")
  existing_note.title = note.title
  existing_note.content = note.content
  db.commit()
  db.refresh(existing_note)
  return existing_note

@router.delete("/{id}")
@limiter.limit("30/minute")
def delete_note(request: Request,id:int, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
  note = db.query(models.Note).filter(models.Note.id == id, models.Note.user_id == current_user.id, models.Note.deleted_at == None).first()
  if not note:
    raise HTTPException(status_code=404, detail="note not found")
  # db.delete(note)
  #adding soft delete
  note.deleted_at = datetime.now(timezone.utc)
  db.commit()
  return {"message": "Note moved to trash"}

@router.patch("/{id}/restore")
@limiter.limit("30/minute")
def restore_note(request: Request, id: int, db: Session = Depends(get_db), current_user : models.User= Depends(get_current_user)):
  note = db.query(models.Note).filter(
    models.Note.id ==id,
    models.Note.user_id == current_user.id,
    models.Note.deleted_at !=None
  ).first()
  if not note:
    raise HTTPException(status_code=404, detail="Note not found in trash")
  note.deleted_at = None
  db.commit()
  db.refresh(note)
  return {"message": "Note restored successfully"}



  
