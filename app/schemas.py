from pydantic import BaseModel



class NoteCreate(BaseModel):
  title:str
  content:str

class UserCreate(BaseModel):
  email:str
  password: str
