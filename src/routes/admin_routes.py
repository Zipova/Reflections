from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import UserResponse, UserStatusUpdate, UserRoleUpdate
from src.services.auth import auth_service

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
        user_id: int, user_status_update: UserStatusUpdate, current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role == Role.admin:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.is_active = user_status_update.is_active
        db.commit()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden: Only administrators can update user status")


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_status(
        user_id: int, user_role_update: UserRoleUpdate, current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    if current_user.role == Role.admin:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user.role = user_role_update.role
        db.commit()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden: Only administrators can change user role")
