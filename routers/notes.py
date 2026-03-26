import aiofiles
import datetime
import json
import os
from fastapi import HTTPException
from typing import Optional
from fastapi import APIRouter
import asyncio
from ..schemas import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Notes"])
data = "data.json"

async def load_notes():
    exists = await asyncio.to_thread(os.path.exists, data)
    if not exists:
        return []
    async with aiofiles.open(data, "r") as f:
        content = await f.read()
        return json.loads(content)
async def save_notes(notes):
    async with aiofiles.open(data, "w") as f:
        await f.write(json.dumps(notes))

@router.get("/")
async def get_notes():
    notes = await load_notes()
    return {"notes": notes}

@router.get("/get-notes-by-title/")
async def get_notes_by_title(title: Optional[str]=None, limit: int = 5):
    notes = await load_notes()
    filtered_notes = [n for n in notes if n["title"] == title]
    if not filtered_notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return [{"id": n["id"], "title": n["title"], "content": n["content"]} for n in filtered_notes[:limit]]

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
 notes = await load_notes()
 new_note = next((note for note in notes if note["id"] == note_id), None)
 if new_note is None:
     raise HTTPException(status_code=404, detail="Note not found")
 return new_note

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate):
    notes = await load_notes()
    new_note_dict = dict(note)
    new_note_dict["id"] = max((n["id"] for n in notes), default=0) + 1
    new_note_dict["created_at"] = datetime.datetime.now().isoformat()
    notes.append(new_note_dict)
    await save_notes(notes)
    return new_note_dict

@router.patch("/{note_id}")
async def update_note(note_id: int, note: NoteUpdate):
    notes = await load_notes()
    updated_note = next((n for n in notes if n["id"] == note_id), None)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    updated_values = note.model_dump(exclude_unset=True)
    updated_note.update(updated_values)
    await save_notes(notes)
    return {"message": f"Note with {note_id} updated successfully!"}

@router.delete("/{note_id}")
async def delete_note(note_id: int):
    notes = await load_notes()
    new_notes =  [n for n in notes if n["id"] != note_id]
    if len(new_notes) == len(notes):
        raise HTTPException(status_code=404, detail="Notes not found")
    await save_notes(new_notes)
    return {"message": f"Note with {note_id} deleted successfully!"}