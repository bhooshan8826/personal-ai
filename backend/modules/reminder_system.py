"""
Reminder scheduling and management system
"""
import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.models import Reminder, Task
from database.schemas import ReminderCreate, ReminderUpdate

logger = logging.getLogger(__name__)


class ReminderSystem:
    """Manage reminders and scheduling"""

    RECURRENCE_PATTERNS = {
        "daily": lambda dt: dt + timedelta(days=1),
        "weekly": lambda dt: dt + timedelta(weeks=1),
        "monthly": lambda dt: dt + timedelta(days=30),
        "none": lambda dt: None,
    }

    @staticmethod
    def create_reminder(
        db: Session,
        user_id: str,
        reminder_data: ReminderCreate
    ) -> Reminder:
        """Create a new reminder"""
        try:
            reminder = Reminder(
                id=str(uuid.uuid4()),
                user_id=user_id,
                task_id=reminder_data.task_id,
                next_trigger=reminder_data.next_trigger,
                recurrence=reminder_data.recurrence or "none",
                is_active=True,
            )
            db.add(reminder)
            db.commit()
            db.refresh(reminder)
            logger.info(f"Reminder created: {reminder.id}")
            return reminder
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating reminder: {e}")
            raise

    @staticmethod
    def get_reminder(
        db: Session,
        reminder_id: str,
        user_id: str
    ) -> Optional[Reminder]:
        """Get reminder by ID"""
        return db.query(Reminder).filter(
            Reminder.id == reminder_id,
            Reminder.user_id == user_id
        ).first()

    @staticmethod
    def list_reminders(
        db: Session,
        user_id: str,
        active_only: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List reminders"""
        try:
            query = db.query(Reminder).filter(Reminder.user_id == user_id)

            if active_only:
                query = query.filter(Reminder.is_active == True)

            total = query.count()
            reminders = query.order_by(Reminder.next_trigger).offset(offset).limit(limit).all()

            return {
                "reminders": reminders,
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        except Exception as e:
            logger.error(f"Error listing reminders: {e}")
            raise

    @staticmethod
    def update_reminder(
        db: Session,
        reminder_id: str,
        user_id: str,
        reminder_data: ReminderUpdate
    ) -> Optional[Reminder]:
        """Update reminder"""
        try:
            reminder = ReminderSystem.get_reminder(db, reminder_id, user_id)
            if not reminder:
                return None

            if reminder_data.next_trigger is not None:
                reminder.next_trigger = reminder_data.next_trigger
            if reminder_data.recurrence is not None:
                reminder.recurrence = reminder_data.recurrence
            if reminder_data.is_active is not None:
                reminder.is_active = reminder_data.is_active

            reminder.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(reminder)
            logger.info(f"Reminder updated: {reminder.id}")
            return reminder
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating reminder: {e}")
            raise

    @staticmethod
    def delete_reminder(db: Session, reminder_id: str, user_id: str) -> bool:
        """Delete reminder"""
        try:
            reminder = ReminderSystem.get_reminder(db, reminder_id, user_id)
            if not reminder:
                return False

            db.delete(reminder)
            db.commit()
            logger.info(f"Reminder deleted: {reminder.id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting reminder: {e}")
            raise

    @staticmethod
    def get_due_reminders(db: Session) -> List[Reminder]:
        """Get reminders that are due"""
        try:
            now = datetime.utcnow()
            return db.query(Reminder).filter(
                Reminder.is_active == True,
                Reminder.next_trigger <= now
            ).all()
        except Exception as e:
            logger.error(f"Error getting due reminders: {e}")
            return []

    @staticmethod
    def trigger_reminder(db: Session, reminder_id: str) -> Optional[Reminder]:
        """Trigger a reminder and schedule next occurrence"""
        try:
            reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
            if not reminder:
                return None

            # Mark as triggered
            reminder.last_triggered = datetime.utcnow()

            # Schedule next trigger if recurring
            if reminder.recurrence and reminder.recurrence != "none":
                pattern_func = ReminderSystem.RECURRENCE_PATTERNS.get(
                    reminder.recurrence
                )
                if pattern_func:
                    new_trigger = pattern_func(reminder.next_trigger)
                    if new_trigger:
                        reminder.next_trigger = new_trigger
                    else:
                        reminder.is_active = False
            else:
                reminder.is_active = False

            reminder.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(reminder)
            logger.info(f"Reminder triggered: {reminder.id}")
            return reminder
        except Exception as e:
            db.rollback()
            logger.error(f"Error triggering reminder: {e}")
            raise

    @staticmethod
    def get_upcoming_reminders(
        db: Session,
        user_id: str,
        hours: int = 24
    ) -> List[Reminder]:
        """Get reminders coming up in next N hours"""
        try:
            now = datetime.utcnow()
            future = now + timedelta(hours=hours)

            return db.query(Reminder).filter(
                Reminder.user_id == user_id,
                Reminder.is_active == True,
                Reminder.next_trigger >= now,
                Reminder.next_trigger <= future
            ).order_by(Reminder.next_trigger).all()
        except Exception as e:
            logger.error(f"Error getting upcoming reminders: {e}")
            return []

    @staticmethod
    def snooze_reminder(
        db: Session,
        reminder_id: str,
        user_id: str,
        minutes: int = 15
    ) -> Optional[Reminder]:
        """Snooze a reminder by N minutes"""
        reminder = ReminderSystem.get_reminder(db, reminder_id, user_id)
        if not reminder:
            return None

        new_trigger = reminder.next_trigger + timedelta(minutes=minutes)
        return ReminderSystem.update_reminder(
            db,
            reminder_id,
            user_id,
            ReminderUpdate(next_trigger=new_trigger)
        )


# Global reminder system instance
_reminder_system = ReminderSystem()


def get_reminder_system() -> ReminderSystem:
    """Get reminder system"""
    return _reminder_system
