from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import SessionLocal
from app.models.project import Project
from app.utils.jwt import get_current_user

router = APIRouter()

class ProjectIn(BaseModel):
    name: str
    description: Optional[str] = None

@router.post("/", response_model=dict)
def create_project(payload: ProjectIn, user=Depends(get_current_user)):
    db = SessionLocal()
    proj = Project(name=payload.name, description=payload.description)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return {"id": proj.id, "name": proj.name, "description": proj.description}

@router.get("/", response_model=List[dict])
def list_projects(user=Depends(get_current_user)):
    db = SessionLocal()
    projs = db.query(Project).all()
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projs]

@router.delete("/{project_id}")
def delete_project(project_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        raise HTTPException(404, "Project not found")
    db.delete(proj)
    db.commit()
    return {"detail": "deleted"}
