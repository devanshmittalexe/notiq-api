from pydantic import BaseModel
from fastapi import FastAPI
from app.database import engine, Base
import app.models as models

class NoteCreate(BaseModel):
    title: str
    content: str

# This creates all tables in the database automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

# This is our fake database for now
notes = [
    {"id": 1, "title": "First note", "content": "Hello Notiq"},
    {"id": 2, "title": "Second note", "content": "FastAPI is cool"},
]

@app.get("/") #this is home url
def root():
    return {"message": "Welcome to Notiq API"}

@app.get("/notes") #thisis next to home url
def get_all_notes():
    return notes

@app.get("/notes/{id}") #going to a particular note by id
def get_note(id:int):
    for note in notes:
        if note["id"]==id:
            return note
    return {"error": "Note not found: GM"}

@app.post("/notes")
def create_note(note: NoteCreate):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "content": note.content
    }
    notes.append(new_note)
    return new_note

@app.put("/notes/{id}")
def update_note(id: int, note: NoteCreate):
    for i, n in enumerate(notes):
        if n["id"] == id:
            notes[i]["title"] = note.title
            notes[i]["content"] = note.content
            return notes[i]
    return {"error": "Note not found"}

@app.delete("/notes/{id}")
def delete_note(id: int):
    for i, n in enumerate(notes):
        if n["id"] == id:
            notes.pop(i)
            return {"message": "Note deleted successfully"}
    return {"error": "Note not found"}
