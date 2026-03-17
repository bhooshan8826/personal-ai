"""
Notes API routes
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database.schemas import NoteCreate, NoteUpdate, NoteResponse
from modules.notes_manager import get_notes_manager

router = APIRouter(prefix="/api/v1/notes", tags=["notes"])
notes_manager = get_notes_manager()


@router.get("", response_model=dict)
async def list_notes(
    archived: bool = False,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List notes"""
    user_id = "default-user"

    result = notes_manager.list_notes(
        db,
        user_id,
        archived=archived,
        limit=limit,
        offset=offset
    )
    return result


@router.post("", response_model=NoteResponse)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    """Create a new note"""
    user_id = "default-user"

    created_note = notes_manager.create_note(db, user_id, note)
    return created_note


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    """Get note by ID"""
    user_id = "default-user"

    note = notes_manager.get_note(db, note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    db: Session = Depends(get_db)
):
    """Update note"""
    user_id = "default-user"

    updated_note = notes_manager.update_note(db, note_id, user_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    """Delete note"""
    user_id = "default-user"

    success = notes_manager.delete_note(db, note_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}


@router.get("/_search", response_model=list)
async def search_notes(
    q: str,
    tags: List[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Search notes"""
    user_id = "default-user"

    results = notes_manager.search_notes(db, user_id, q, tags=tags)
    return results


@router.put("/{note_id}/archive", response_model=NoteResponse)
async def archive_note(
    note_id: str,
    db: Session = Depends(get_db)
):
    """Archive note"""
    user_id = "default-user"

    note = notes_manager.archive_note(db, note_id, user_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/tags/{tag}", response_model=list)
async def get_notes_by_tag(
    tag: str,
    db: Session = Depends(get_db)
):
    """Get notes by tag"""
    user_id = "default-user"

    notes = notes_manager.get_notes_by_tag(db, user_id, tag)
    return notes
