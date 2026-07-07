from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.auth import router as auth_router
from app.upload import router as upload_router
from app.history import router as history_router
from app.ats import router as ats_router
from app.dashboard import router as dashboard_router
from app.profile import router as profile_router
from app.report import router as report_router

# Import models so SQLAlchemy creates tables
import app.models

# ==========================================
# Create Database Tables
# ==========================================

Base.metadata.create_all(bind=engine)

# ==========================================
# FastAPI App
# ==========================================

app = FastAPI(
    title="AI Resume Analyser API",
    description="AI-powered ATS Resume Analyzer using FastAPI, NLP and Gemini AI",
    version="1.0.0"
)

# ==========================================
# CORS Configuration
# ==========================================

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# Include Routers
# ==========================================

app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(history_router)
app.include_router(ats_router)
app.include_router(dashboard_router)
app.include_router(profile_router)
app.include_router(report_router)

# ==========================================
# Home Route
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume Analyser API",
        "status": "Running"
    }

# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "database": "Connected"
    }
