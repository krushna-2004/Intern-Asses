from fastapi import FastAPI
from .config import settings
from .routes import auth_routes, project_routes, task_routes

def create_app():
    app = FastAPI(title="Project Management Tool - API")
    app.include_router(auth_routes.router, prefix="/api/auth")
    app.include_router(project_routes.router, prefix="/api/projects")
    app.include_router(task_routes.router, prefix="/api/tasks")
    return app

app = create_app()
