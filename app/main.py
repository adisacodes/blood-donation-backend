from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
# Temporarily commented out to stop other files from crashing your auth setup:
# from app.models import models
from app.routers import auth  #, donors, requests, admin

# Create database tables cleanly for the models Python has loaded
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Management System")

# Configure CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIXED: Changed prefix from "/auth" to "/api/auth" to match your frontend requests
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# Temporarily commented out:
# app.include_router(donors.router, prefix="/api/donors", tags=["Donors"])
# app.include_router(requests.router, prefix="/api/requests", tags=["Requests"])
# app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"message": "Welcome to Blood Donation API 🩸 - Auth Mode"}