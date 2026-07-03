from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ==========================
# USER
# ==========================

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================
# JWT TOKEN
# ==========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# ==========================
# RESUME UPLOAD
# ==========================

class ResumeUploadResponse(BaseModel):
    message: str
    filename: str


# ==========================
# ATS RESULT
# ==========================

class ATSResponse(BaseModel):
    ats_score: float

    matched_skills: List[str]

    missing_skills: List[str]

    suggestions: List[str]

    interview_questions: List[str]


# ==========================
# HISTORY
# ==========================

class ResumeHistoryResponse(BaseModel):
    id: int

    resume_name: str

    jd_title: Optional[str]

    company: Optional[str]

    ats_score: float

    uploaded_at: datetime

    class Config:
        from_attributes = True
