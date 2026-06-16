from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.routers import auth, donors, requests, admin
from app.database import engine
from app.models import models
from app.utils.seed_admin import seed_super_admin

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",

        "https://blood-donations-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(donors.router, prefix="/api/donors", tags=["Donors"])
app.include_router(requests.router, prefix="/api/blood-requests", tags=["Blood Requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Welcome to Blood Donation API 🩸"}

@app.on_event("startup")
def seed_admin_on_startup():
    with Session(engine) as db:
        seed_super_admin(db)
    print("✅ Admin seeding completed!")