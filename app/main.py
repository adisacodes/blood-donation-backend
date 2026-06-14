from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import models
from app.models.user import User
from app.routers import auth, donors, requests, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Management System")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(donors.router, prefix="/donors", tags=["Donors"])
app.include_router(requests.router, prefix="/requests", tags=["Requests"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"message": "Welcome to Blood Donation API 🩸"}