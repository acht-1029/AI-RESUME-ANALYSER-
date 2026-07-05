from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ResumeHistory
from app.dependencies import get_current_user

from services.ats_service import ATSService

router = APIRouter(
    prefix="/ats",
    tags=["ATS Analysis"]
)


@router.post("/analyze/{resume_id}")
def analyze_resume(
    resume_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(
        ResumeHistory
    ).filter(
        ResumeHistory.id == resume_id,
        ResumeHistory.user_id == current_user.id
    ).first()

    if history is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    result = ATSService.analyze_resume(
        file_path=history.resume_path,
        job_description=history.job_description
    )

    history.ats_score = result["ats_score"]

    history.matched_skills = ",".join(
        result["matched_skills"]
    )

    history.missing_skills = ",".join(
        result["missing_skills"]
    )

    history.suggestions = "\n".join(
        result["suggestions"]
    )

    history.interview_questions = "\n".join(
        result["interview_questions"]
    )

    db.commit()

    return {
        "message": "Analysis Completed",

        "resume_id": history.id,

        "ats_score": history.ats_score,

        "matched_skills": result["matched_skills"],

        "missing_skills": result["missing_skills"],

        "suggestions": result["suggestions"],

        "interview_questions": result["interview_questions"],

        "ai_feedback": result["ai_feedback"],
    }
