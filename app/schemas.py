from pydantic import BaseModel, EmailStr

class OrgCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str

class OrgQuery(BaseModel):
    organization_name: str

class AdminLogin(BaseModel):
    admin: EmailStr
    password: str
