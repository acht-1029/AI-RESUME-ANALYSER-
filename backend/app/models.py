from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship(
        "ResumeHistory",
        back_populates="user",
        cascade="all, delete"
    )


class ResumeHistory(Base):
    __tablename__ = "resume_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    resume_name = Column(String(255))

    resume_path = Column(String(255))

    jd_title = Column(String(255))

    company = Column(String(255))

    ats_score = Column(Float)

    matched_skills = Column(Text)

    missing_skills = Column(Text)

    suggestions = Column(Text)

    interview_questions = Column(Text)

    uploaded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="resumes"
    )
