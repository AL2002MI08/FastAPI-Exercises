from typing import List
from fastapi import APIRouter
from ..schemas import NoteCreate, NoteUpdate
from ..services import notes_service

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/", response_model=List[NoteCreate])
async def get_notes():
    return await notes_service.get_notes()

@router.get("/{note_id}")
async def get_note(note_id: int):
    return await notes_service.get_note(note_id)

@router.post("/", response_model=List[NoteCreate])
async def create_note(note: NoteCreate):
    return await notes_service.create_note(note)

@router.patch("/{note_id}", response_model=NoteCreate)
async def update_note(note_id: int, note: NoteUpdate):
    return await notes_service.update_note(note_id, note)

@router.delete("/{note_id}", status_code=204)
async def delete_note(note_id: int):
    return await notes_service.delete_note(note_id)