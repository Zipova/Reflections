from fastapi import APIRouter, HTTPException, Depends, status

from src.database.db import SessionLocal
from src.database.models import User
from src.schemas import UserResponse, UserStatusUpdate
from src.services.auth import auth_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put("/users/{username}/status", response_model=UserResponse)
def update_user_status(
    username: str, user_status_update: UserStatusUpdate, current_user: User = Depends(auth_service.get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden: Only administrators can update user status")
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        db.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = user_status_update.is_active
    db.commit()
    db.refresh(user)
    db.close()

    return user
