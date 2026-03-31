import datetime
import aiofiles
import json
import os
from fastapi import HTTPException
from typing import Optional
from ..schemas import NoteCreate, NoteUpdate

data = "data.json"

async def load_notes():
    if not os.path.exists(data):
        return []
    async with aiofiles.open(data, "r") as f:
        content = await f.read()
        notes = json.loads(content)
        return [NoteCreate(**note) for note in notes]

async def save_notes(notes):
    async with aiofiles.open(data, "w") as f:
        await f.write(json.dumps(notes))

async def get_notes(title: Optional[str]=None, limit: int = 5):
    notes = await load_notes()
    if title is not None:
        notes = [n for n in notes if n.title == title]
    return  notes[:limit]

async def get_note(note_id: int):
 notes = await load_notes()
 new_note = next((note for note in notes if note.id == note_id), None)
 if new_note is None:
     raise HTTPException(status_code=404, detail="Note not found")
 return new_note

async def create_note(note: NoteCreate):
    notes = await load_notes()
    new_id = max((n.id for n in notes), default=0) + 1
    new_note = NoteCreate(
        id=new_id,
        title=note.title,
        content=note.content,
        created_at= datetime.datetime.now(),
    )
    notes.append(new_note)
    await save_notes(notes)
    return new_note

async def update_note(note_id: int, note: NoteUpdate):
    notes = await load_notes()
    updated_note = next((n for n in notes if n.id == note_id), None)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    updated_values = note.model_dump(exclude_unset=True)
    updated_note.update(updated_values)
    await save_notes(notes)
    return {"message": f"Note with {note_id} updated successfully!"}

async def delete_note(note_id: int):
    notes = await load_notes()
    new_notes =  [n for n in notes if n["id"] != note_id]
    if len(new_notes) == len(notes):
        raise HTTPException(status_code=404, detail="Notes not found")
    await save_notes(new_notes)
    return {"message": f"Note with {note_id} deleted successfully!"}