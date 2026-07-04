from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, ResumeHistory
from app.security import decode_access_token
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = (
        db.query(ResumeHistory)
        .filter(
            ResumeHistory.user_id == current_user.id
        )
        .order_by(
            ResumeHistory.uploaded_at.desc()
        )
        .all()
    )

    return history
