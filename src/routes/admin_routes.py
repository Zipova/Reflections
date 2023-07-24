from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import SQLALCHEMY_DATABASE_URL
from database.models import User
from schemas import UserResponse, UserUpdate, UserStatusUpdate
from authentication import get_current_user

app = FastAPI()


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Route to get the user profile by their unique username


@app.get("/profile/{username}", response_model=UserResponse, tags=["User Profile"])
def get_user_profile(username: str, current_user: User = Depends(get_current_user)):
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user

# Route to update the user profile


@app.put("/profile/{username}", response_model=UserResponse, tags=["User Profile"])
def update_user_profile(username: str, user_update: UserUpdate, current_user: User = Depends(get_current_user)):
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

# Route to update the user status (for administrators)


@app.put("/admin/users/{username}/status", response_model=UserResponse, tags=["Admin"])
def update_user_status(username: str, user_status_update: UserStatusUpdate, current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:  
        raise HTTPException(
            status_code=403, detail="Forbidden: Only administrators can update user status")

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = user_status_update.is_active
    db.commit()
    db.refresh(user)
    db.close()

    return user

