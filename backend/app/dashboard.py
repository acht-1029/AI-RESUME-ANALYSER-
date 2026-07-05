from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import ResumeHistory
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    resumes = db.query(ResumeHistory).filter(
        ResumeHistory.user_id == current_user.id
    ).all()

    total_resumes = len(resumes)

    average_score = db.query(
        func.avg(ResumeHistory.ats_score)
    ).filter(
        ResumeHistory.user_id == current_user.id
    ).scalar()

    highest_score = db.query(
        func.max(ResumeHistory.ats_score)
    ).filter(
        ResumeHistory.user_id == current_user.id
    ).scalar()

    latest_resume = db.query(
        ResumeHistory
    ).filter(
        ResumeHistory.user_id == current_user.id
    ).order_by(
        ResumeHistory.uploaded_at.desc()
    ).first()

    return {

        "total_resumes": total_resumes,

        "average_score": round(
            average_score or 0,
            2
        ),

        "highest_score": highest_score or 0,

        "latest_resume": latest_resume.resume_name if latest_resume else None,

        "latest_score": latest_resume.ats_score if latest_resume else 0

    }
