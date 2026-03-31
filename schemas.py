from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    id: int
    title: str
    content: str
    created_at: Optional[datetime] = datetime.now()

    def update(self, updated_values):
        pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

class MessageResponse(BaseModel):
    message: str