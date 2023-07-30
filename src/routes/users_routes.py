from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import User
from src.database.db import SessionLocal, get_db
from src.schemas import UserResponse, UserUpdate
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["User Profile"])


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/me", response_model=UserResponse)
def update_my_profile(user_update: UserUpdate,
                        current_user: User = Depends(auth_service.get_current_user),
                        db: Session = Depends(get_db)):
    current_user.username = user_update.username

    #for key, value in user_update.dict(exclude_unset=True).items():
    #   setattr(current_user, key, value)

    db.commit()
    #db.refresh(current_user)

    return current_user
