import os
import shutil
from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
    status
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database import get_db
from models import User, ResumeHistory
from security import decode_access_token

# ==========================================
# Router
# ==========================================

router = APIRouter(
    prefix="/resume",
    tags=["Resume Upload"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx"]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


# ==========================================
# Get Current User
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = decode_access_token(token)

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ==========================================
# Upload Resume
# ==========================================

@router.post("/upload")
async def upload_resume(

    file: UploadFile = File(...),

    jd_title: str = Form(...),

    company: str = Form(...),

    job_description: str = Form(...),
 
    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="Maximum file size is 5MB."
        )

    filename = f"{datetime.utcnow().timestamp()}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(filepath, "wb") as buffer:
        buffer.write(content)

    history = ResumeHistory(

        user_id=current_user.id,

        resume_name=file.filename,

        resume_path=filepath,

        jd_title=jd_title,

        job_description=job_description,

        company=company,

        ats_score=0,

        matched_skills="",

        missing_skills="",

        suggestions="",

        interview_questions=""

    )

    db.add(history)

    db.commit()

    db.refresh(history)

    return {

        "message": "Resume uploaded successfully",

        "resume_id": history.id,

        "filename": file.filename,

        "company": company,

        "job_title": jd_title

    }
