"""
Reminders API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import ReminderCreate, ReminderUpdate, ReminderResponse
from modules.reminder_system import get_reminder_system

router = APIRouter(prefix="/api/v1/reminders", tags=["reminders"])
reminder_system = get_reminder_system()


@router.get("", response_model=dict)
async def list_reminders(
    active_only: bool = True,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List reminders"""
    user_id = "default-user"

    result = reminder_system.list_reminders(
        db,
        user_id,
        active_only=active_only,
        limit=limit,
        offset=offset
    )
    return result


@router.post("", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db)
):
    """Create a new reminder"""
    user_id = "default-user"

    created_reminder = reminder_system.create_reminder(db, user_id, reminder)
    return created_reminder


@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: str,
    db: Session = Depends(get_db)
):
    """Get reminder by ID"""
    user_id = "default-user"

    reminder = reminder_system.get_reminder(db, reminder_id, user_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: str,
    reminder_data: ReminderUpdate,
    db: Session = Depends(get_db)
):
    """Update reminder"""
    user_id = "default-user"

    updated_reminder = reminder_system.update_reminder(
        db, reminder_id, user_id, reminder_data
    )
    if not updated_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_reminder


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: str,
    db: Session = Depends(get_db)
):
    """Delete reminder"""
    user_id = "default-user"

    success = reminder_system.delete_reminder(db, reminder_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder deleted successfully"}


@router.get("/_due", response_model=list)
async def get_due_reminders(db: Session = Depends(get_db)):
    """Get due reminders"""
    reminders = reminder_system.get_due_reminders(db)
    return reminders


@router.get("/_upcoming", response_model=list)
async def get_upcoming_reminders(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get upcoming reminders"""
    user_id = "default-user"

    reminders = reminder_system.get_upcoming_reminders(db, user_id, hours=hours)
    return reminders


@router.post("/{reminder_id}/_trigger", response_model=ReminderResponse)
async def trigger_reminder(
    reminder_id: str,
    db: Session = Depends(get_db)
):
    """Trigger a reminder"""
    reminder = reminder_system.trigger_reminder(db, reminder_id)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder


@router.post("/{reminder_id}/_snooze", response_model=ReminderResponse)
async def snooze_reminder(
    reminder_id: str,
    minutes: int = 15,
    db: Session = Depends(get_db)
):
    """Snooze a reminder"""
    user_id = "default-user"

    reminder = reminder_system.snooze_reminder(db, reminder_id, user_id, minutes)
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder
