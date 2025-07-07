from fastapi import FastAPI
from app.routers import organizations, admin, master

app = FastAPI()

app.include_router(organizations.router)
app.include_router(admin.router)
app.include_router(master.router)
