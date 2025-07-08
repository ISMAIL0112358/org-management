from fastapi import APIRouter, HTTPException, Depends
from app.database import create_master_db, get_org_db_name, create_org_db
from app.schemas import OrgCreate, OrgQuery
from app.auth import get_password_hash, pwd_context, get_current_master_admin
import psycopg2

router = APIRouter()

@router.post("/Org/create")
def create_organization(payload: OrgCreate, current_user: dict = Depends(get_current_master_admin)):

    create_master_db()

    if get_org_db_name(payload.organization_name):
        raise HTTPException(status_code=400, detail="Organization already exists")

    created_db_name = create_org_db(payload.organization_name, payload.email, payload.password, pwd_context)

    from app.config import settings

    conn = psycopg2.connect(
        dbname=settings.master_db_name, user=settings.master_db_user, password=settings.master_db_password, host=settings.master_db_host, port=settings.master_db_port
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO organizations (name, db_name, admin_email) VALUES (%s, %s, %s)",
                (payload.organization_name.lower(), created_db_name, payload.email))
    conn.commit()
    conn.close()
    return {"message": "Organization created successfully"}

@router.post("/Org/get")
def get_organization(payload: OrgQuery, current_user: dict = Depends(get_current_master_admin)):
    db_name = get_org_db_name(payload.organization_name)
    if not db_name:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"organization_name": payload.organization_name, "db_name": db_name}
