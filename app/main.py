from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, donors, requests, admin
from app.database import engine
from app.models import models

# Initialize Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Management System")

# CORS Middleware Configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🌟 FIXED PREFIXES: Added "/api" to all router paths to align with the frontend services
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(donors.router, prefix="/api/donors", tags=["Donors"])
app.include_router(requests.router, prefix="/api/requests", tags=["Requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Welcome to Blood Donation API 🩸"}