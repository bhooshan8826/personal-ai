"""
Task API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas import TaskCreate, TaskUpdate, TaskResponse
from modules.task_manager import get_task_manager

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
task_manager = get_task_manager()


@router.get("", response_model=dict)
async def list_tasks(
    status: str = None,
    priority: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List tasks"""
    # TODO: Get user_id from auth
    user_id = "default-user"

    result = task_manager.list_tasks(
        db,
        user_id,
        status=status,
        priority=priority,
        limit=limit,
        offset=offset
    )
    return result


@router.post("", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """Create a new task"""
    # TODO: Get user_id from auth
    user_id = "default-user"

    created_task = task_manager.create_task(db, user_id, task)
    return created_task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Get task by ID"""
    user_id = "default-user"

    task = task_manager.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """Update task"""
    user_id = "default-user"

    updated_task = task_manager.update_task(db, task_id, user_id, task_data)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Delete task"""
    user_id = "default-user"

    success = task_manager.delete_task(db, task_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.put("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    """Mark task as complete"""
    user_id = "default-user"

    task = task_manager.complete_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/_search", response_model=list)
async def search_tasks(
    q: str,
    db: Session = Depends(get_db)
):
    """Search tasks"""
    user_id = "default-user"

    results = task_manager.search_tasks(db, user_id, q)
    return results


@router.get("/_stats", response_model=dict)
async def get_task_stats(db: Session = Depends(get_db)):
    """Get task statistics"""
    user_id = "default-user"

    stats = task_manager.get_task_stats(db, user_id)
    return stats
