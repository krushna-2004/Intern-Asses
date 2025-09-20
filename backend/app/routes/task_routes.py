from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.database import SessionLocal
from app.models.task import Task
from app.models.project import Project
from app.utils.jwt import get_current_user

router = APIRouter()

class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None

@router.post("/", response_model=dict)
def create_task(payload: TaskIn, user=Depends(get_current_user)):
    db = SessionLocal()
    if payload.project_id:
        p = db.query(Project).filter(Project.id == payload.project_id).first()
        if not p:
            raise HTTPException(400, "Invalid project")
    t = Task(title=payload.title, description=payload.description, due_date=payload.due_date, project_id=payload.project_id, assignee_id=payload.assignee_id)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "title": t.title, "status": t.status}

@router.get("/", response_model=List[dict])
def list_tasks(user=Depends(get_current_user)):
    db = SessionLocal()
    ts = db.query(Task).filter(Task.is_deleted == False).all()
    out = []
    for t in ts:
        overdue = t.due_date and t.due_date < datetime.utcnow()
        out.append({"id": t.id, "title": t.title, "status": t.status, "overdue": bool(overdue)})
    return out

@router.patch("/{task_id}")
def update_task(task_id: int, payload: TaskIn, user=Depends(get_current_user)):
    db = SessionLocal()
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    for k,v in payload.dict(exclude_unset=True).items():
        setattr(t, k, v)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "title": t.title, "status": t.status}

@router.delete("/{task_id}")
def delete_task(task_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    t.is_deleted = True
    db.commit()
    return {"detail": "soft-deleted"}
