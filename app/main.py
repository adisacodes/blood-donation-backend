from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models.user import User 
from app.routers import auth, donors, requests, admin
from app.utils.seed_admin import seed_super_admin

# Build database tables using metadata schemas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blood Donation Management System")

# 1. Global CORS Setup (Covers both local ports 5173 and 5174 dynamically)
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

# 2. Strict Preflight Guard (Safely mirrors the active frontend origin)
@app.middleware("http")
async def handle_preflight(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
        origin = request.headers.get("Origin")
        
        # Only echo back the origin if it matches our local development environments
        if origin in ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"]:
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            response.headers["Access-Control-Allow-Origin"] = "http://localhost:5174"
            
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept, Origin"
        return response
        
    return await call_next(request)

# Automated Database Seed Event on API Startup
@app.on_event("startup")
def on_startup():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        seed_super_admin(db)
    finally:
        db.close()

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(donors.router, prefix="/api/donors", tags=["Donors"])
app.include_router(requests.router, prefix="/api/requests", tags=["Requests"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Welcome to Blood Donation API 🩸 - Production Mode"}