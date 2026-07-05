from io import BytesIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from app.database import get_db
from app.models import ResumeHistory
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


@router.get("/{resume_id}")
def generate_report(
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

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>AI Resume Analysis Report</b>", styles["Heading1"])
    )

    story.append(
        Paragraph(f"<b>Resume:</b> {history.resume_name}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>Company:</b> {history.company}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>Job Title:</b> {history.jd_title}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>ATS Score:</b> {history.ats_score}", styles["BodyText"])
    )

    story.append(
        Paragraph(
            f"<b>Matched Skills:</b><br/>{history.matched_skills}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Missing Skills:</b><br/>{history.missing_skills}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Suggestions:</b><br/>{history.suggestions}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Interview Questions:</b><br/>{history.interview_questions}",
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            f"attachment; filename=ATS_Report_{resume_id}.pdf"
        }
    )
