from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginIn(BaseModel):
    email: str
    password: str

# WARNING: This is a minimal demo auth - DO NOT use in production.
@router.post("/login")
def login(data: LoginIn):
    if data.email.endswith("@example.com"):
        role = "Developer"
        if data.email.startswith("admin"):
            role = "Admin"
        elif data.email.startswith("manager"):
            role = "Manager"
        # return a simple token representing role
        token = f"{role.lower()}-token"
        return {"access_token": token, "token_type": "bearer", "role": role}
    raise HTTPException(status_code=400, detail="Invalid credentials")
