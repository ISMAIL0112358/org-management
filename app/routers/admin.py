from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_org_db_name
from app.auth import verify_password, create_access_token, pwd_context
import psycopg2
from app.config import settings

router = APIRouter()

@router.post("/admin/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    org_name = None
    if "@" in form_data.username:
        domain = form_data.username.split("@")[1]
        org_name = domain.split(".")[0] # Extracts 'myorg' from 'myorg.com'
    db_name = get_org_db_name(org_name)
    if not db_name:
        raise HTTPException(status_code=404, detail="Organization not found")

    org_conn = psycopg2.connect(
        dbname=db_name, user=settings.master_db_user, password=settings.master_db_password, host=settings.master_db_host, port=settings.master_db_port
    )
    cur = org_conn.cursor()
    cur.execute("SELECT hashed_password FROM admin WHERE email=%s", (form_data.username,))
    row = cur.fetchone()
    org_conn.close()
    if not row or not verify_password(form_data.password, row[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}
