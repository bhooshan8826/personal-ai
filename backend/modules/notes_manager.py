"""
Notes management module
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from database.models import Note
from database.schemas import NoteCreate, NoteUpdate

logger = logging.getLogger(__name__)


class NotesManager:
    """Manage notes"""

    @staticmethod
    def create_note(
        db: Session,
        user_id: str,
        note_data: NoteCreate
    ) -> Note:
        """Create a new note"""
        try:
            note = Note(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=note_data.title,
                content=note_data.content,
                tags=note_data.tags,
            )
            db.add(note)
            db.commit()
            db.refresh(note)
            logger.info(f"Note created: {note.id}")
            return note
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating note: {e}")
            raise

    @staticmethod
    def get_note(db: Session, note_id: str, user_id: str) -> Optional[Note]:
        """Get note by ID"""
        return db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()

    @staticmethod
    def list_notes(
        db: Session,
        user_id: str,
        archived: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List notes"""
        try:
            query = db.query(Note).filter(
                Note.user_id == user_id,
                Note.is_archived == archived
            )
            total = query.count()
            notes = query.order_by(desc(Note.created_at)).offset(offset).limit(limit).all()

            return {
                "notes": notes,
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        except Exception as e:
            logger.error(f"Error listing notes: {e}")
            raise

    @staticmethod
    def search_notes(
        db: Session,
        user_id: str,
        query: str,
        tags: Optional[List[str]] = None
    ) -> List[Note]:
        """Search notes by content or tags"""
        try:
            search_term = f"%{query}%"
            q = db.query(Note).filter(
                Note.user_id == user_id,
                or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term)
                )
            )

            # Filter by tags if provided
            if tags:
                for tag in tags:
                    q = q.filter(Note.tags.contains([tag]))

            return q.order_by(desc(Note.created_at)).all()
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return []

    @staticmethod
    def update_note(
        db: Session,
        note_id: str,
        user_id: str,
        note_data: NoteUpdate
    ) -> Optional[Note]:
        """Update note"""
        try:
            note = NotesManager.get_note(db, note_id, user_id)
            if not note:
                return None

            if note_data.title is not None:
                note.title = note_data.title
            if note_data.content is not None:
                note.content = note_data.content
            if note_data.tags is not None:
                note.tags = note_data.tags
            if note_data.is_archived is not None:
                note.is_archived = note_data.is_archived

            note.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(note)
            logger.info(f"Note updated: {note.id}")
            return note
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating note: {e}")
            raise

    @staticmethod
    def delete_note(db: Session, note_id: str, user_id: str) -> bool:
        """Delete note"""
        try:
            note = NotesManager.get_note(db, note_id, user_id)
            if not note:
                return False

            db.delete(note)
            db.commit()
            logger.info(f"Note deleted: {note.id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting note: {e}")
            raise

    @staticmethod
    def archive_note(db: Session, note_id: str, user_id: str) -> Optional[Note]:
        """Archive note"""
        return NotesManager.update_note(
            db,
            note_id,
            user_id,
            NoteUpdate(is_archived=True)
        )

    @staticmethod
    def get_notes_by_tag(
        db: Session,
        user_id: str,
        tag: str
    ) -> List[Note]:
        """Get notes by tag"""
        try:
            return db.query(Note).filter(
                Note.user_id == user_id,
                Note.tags.contains([tag])
            ).all()
        except Exception as e:
            logger.error(f"Error getting notes by tag: {e}")
            return []


# Global notes manager instance
_notes_manager = NotesManager()


def get_notes_manager() -> NotesManager:
    """Get notes manager"""
    return _notes_manager
