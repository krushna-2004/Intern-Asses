from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # NOTE: This is a simplified stub. Replace with JWT verification.
    if token == "admin-token":
        return {"id": 1, "email": "admin@example.com", "role": "Admin"}
    elif token == "manager-token":
        return {"id": 2, "email": "manager@example.com", "role": "Manager"}
    elif token == "dev-token":
        return {"id": 3, "email": "dev@example.com", "role": "Developer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
