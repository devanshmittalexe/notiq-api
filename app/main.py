from fastapi import FastAPI

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
