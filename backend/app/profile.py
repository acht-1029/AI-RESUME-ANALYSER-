from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.dependencies import get_current_user
from app.security import hash_password, verify_password
from pydantic import BaseModel

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


class UpdateProfile(BaseModel):
    full_name: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


@router.get("/")
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email
    }


@router.put("/update")
def update_profile(
    data: UpdateProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    current_user.full_name = data.full_name

    db.commit()

    db.refresh(current_user)

    return {
        "message": "Profile updated successfully."
    }


@router.put("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    if not verify_password(
        data.current_password,
        current_user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect."
        )

    current_user.password = hash_password(
        data.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully."
    }
