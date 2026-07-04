from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User, ResumeHistory
from security import decode_access_token

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    email = decode_access_token(token)

    if email is None:
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
