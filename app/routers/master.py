from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_master_admin, create_master_admin
from app.auth import verify_password, create_access_token, pwd_context
from app.schemas import AdminLogin

router = APIRouter()

@router.post("/master/register")
def register_master_admin(payload: AdminLogin):
    existing_admin = get_master_admin(payload.admin)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Master admin already exists")
    
    hashed_password = pwd_context.hash(payload.password)
    create_master_admin(payload.admin, hashed_password)
    return {"message": "Master admin registered successfully"}

@router.post("/master/login")
def master_login(form_data: OAuth2PasswordRequestForm = Depends()):
    master_admin = get_master_admin(form_data.username)
    if not master_admin or not verify_password(form_data.password, master_admin["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": form_data.username, "role": "master_admin"})
    return {"access_token": token, "token_type": "bearer"}
