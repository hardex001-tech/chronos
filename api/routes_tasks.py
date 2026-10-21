from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database.db import get_connection

router = APIRouter(prefix="/api/tasks", tags=["Tasks & Streaks"])

class TaskCreate(BaseModel):
    title: str
    category: Optional[str] = "Streak"
    target_link: Optional[str] = None

@router.get("")
def list_tasks():
    """List all daily streaks and university tasks."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, streak_count, completed_today, last_completed, target_link FROM tasks ORDER BY id ASC;")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

@router.post("")
def create_task(task: TaskCreate):
    """Add a new streak or learning milestone."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, category, streak_count, completed_today, target_link)
        VALUES (?, ?, 0, 0, ?);
    """, (task.title, task.category, task.target_link))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "message": "Task created"}

@router.post("/{task_id}/toggle")
def toggle_task(task_id: int):
    """Toggle completion and update streak counter."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT completed_today, streak_count FROM tasks WHERE id = ?;", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return {"error": "Task not found"}

    curr_completed = row["completed_today"]
    curr_streak = row["streak_count"]

    if curr_completed == 0:
        new_completed = 1
        new_streak = curr_streak + 1
        last_date = date.today().isoformat()
    else:
        new_completed = 0
        new_streak = max(0, curr_streak - 1)
        last_date = None

    cursor.execute("""
        UPDATE tasks
        SET completed_today = ?, streak_count = ?, last_completed = ?
        WHERE id = ?;
    """, (new_completed, new_streak, last_date, task_id))
    conn.commit()
    conn.close()
    return {"completed_today": new_completed, "streak_count": new_streak}

@router.delete("/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?;", (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted"}
