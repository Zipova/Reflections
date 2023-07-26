from fastapi import APIRouter, Depends, HTTPException
from database.models import User
from src.database.db import SessionLocal
from src.schemas import UserResponse, UserUpdate
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["User Profile"])


@router.get("/{username}", response_model=UserResponse)
def get_user_profile(username: str, current_user: User = Depends(auth_service.get_current_user)):
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@router.put("/{username}", response_model=UserResponse)
def update_user_profile(username: str, user_update: UserUpdate, current_user: User = Depends(auth_service.get_current_user)):
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Forbidden")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    db.close()

    return user
