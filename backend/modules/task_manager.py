"""
Task management module
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database.models import Task, User
from database.schemas import TaskCreate, TaskUpdate, TaskResponse

logger = logging.getLogger(__name__)


class TaskManager:
    """Manage tasks"""

    @staticmethod
    def create_task(
        db: Session,
        user_id: str,
        task_data: TaskCreate
    ) -> Task:
        """Create a new task"""
        try:
            task = Task(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=task_data.title,
                description=task_data.description,
                priority=task_data.priority,
                deadline=task_data.deadline,
                tags=task_data.tags,
                status="pending",
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            logger.info(f"Task created: {task.id}")
            return task
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating task: {e}")
            raise

    @staticmethod
    def get_task(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Get task by ID"""
        return db.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

    @staticmethod
    def list_tasks(
        db: Session,
        user_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List tasks with filters"""
        try:
            query = db.query(Task).filter(Task.user_id == user_id)

            if status:
                query = query.filter(Task.status == status)

            if priority:
                query = query.filter(Task.priority == priority)

            # Count total
            total = query.count()

            # Apply ordering and pagination
            tasks = query.order_by(desc(Task.created_at)).offset(offset).limit(limit).all()

            return {
                "tasks": tasks,
                "total": total,
                "limit": limit,
                "offset": offset,
            }
        except Exception as e:
            logger.error(f"Error listing tasks: {e}")
            raise

    @staticmethod
    def update_task(
        db: Session,
        task_id: str,
        user_id: str,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Update task"""
        try:
            task = TaskManager.get_task(db, task_id, user_id)
            if not task:
                return None

            # Update only provided fields
            if task_data.title is not None:
                task.title = task_data.title
            if task_data.description is not None:
                task.description = task_data.description
            if task_data.priority is not None:
                task.priority = task_data.priority
            if task_data.status is not None:
                task.status = task_data.status
            if task_data.deadline is not None:
                task.deadline = task_data.deadline
            if task_data.tags is not None:
                task.tags = task_data.tags

            task.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(task)
            logger.info(f"Task updated: {task.id}")
            return task
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating task: {e}")
            raise

    @staticmethod
    def complete_task(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Mark task as complete"""
        return TaskManager.update_task(
            db,
            task_id,
            user_id,
            TaskUpdate(status="completed")
        )

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str) -> bool:
        """Delete task"""
        try:
            task = TaskManager.get_task(db, task_id, user_id)
            if not task:
                return False

            db.delete(task)
            db.commit()
            logger.info(f"Task deleted: {task.id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting task: {e}")
            raise

    @staticmethod
    def get_overdue_tasks(db: Session, user_id: str) -> List[Task]:
        """Get overdue tasks"""
        try:
            return db.query(Task).filter(
                Task.user_id == user_id,
                Task.status == "pending",
                Task.deadline < datetime.utcnow()
            ).all()
        except Exception as e:
            logger.error(f"Error getting overdue tasks: {e}")
            return []

    @staticmethod
    def search_tasks(db: Session, user_id: str, query: str) -> List[Task]:
        """Search tasks by title or description"""
        try:
            search_term = f"%{query}%"
            return db.query(Task).filter(
                Task.user_id == user_id,
                (Task.title.ilike(search_term) | Task.description.ilike(search_term))
            ).all()
        except Exception as e:
            logger.error(f"Error searching tasks: {e}")
            return []

    @staticmethod
    def get_task_stats(db: Session, user_id: str) -> Dict[str, Any]:
        """Get task statistics"""
        try:
            all_tasks = db.query(Task).filter(Task.user_id == user_id).all()
            completed = [t for t in all_tasks if t.status == "completed"]
            pending = [t for t in all_tasks if t.status == "pending"]
            high_priority = [t for t in pending if t.priority == "high"]

            return {
                "total": len(all_tasks),
                "completed": len(completed),
                "pending": len(pending),
                "high_priority": len(high_priority),
                "completion_rate": len(completed) / len(all_tasks) if all_tasks else 0,
            }
        except Exception as e:
            logger.error(f"Error getting task stats: {e}")
            return {}


# Global task manager instance
_task_manager = TaskManager()


def get_task_manager() -> TaskManager:
    """Get task manager"""
    return _task_manager
