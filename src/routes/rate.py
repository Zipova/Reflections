
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
)

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import AvgRateResponse, RateModel, RateResponseModel
from src.repository import photos as repository_photos
from src.repository import rate as repository_rating
from src.services.auth import auth_service
from src.services.roles import RolesChecker

router = APIRouter(prefix="/rating", tags=["rating"])

allowed_edit_rating = RolesChecker([Role.admin, Role.moderator])


@router.get("/", response_model=List[RateResponseModel],
            dependencies=([Depends(allowed_edit_rating)]))
async def get_rating(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db)):
    ratings = await repository_rating.get_rating(limit=limit, offset=offset, db=db)
    return ratings


@router.post("/", response_model=RateResponseModel, status_code=status.HTTP_201_CREATED)
async def rate_photo(photo_rating: RateModel, current_user: User = Depends(auth_service.get_current_user),
                     db: Session = Depends(get_db)):
    photo = await repository_photos.get_photo(photo_rating.photo_id, db)
    if photo.user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot rate your own photo")
    if current_user.id in photo.rated_by:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already rated this photo")
    rating = await repository_rating.create_rating(photo, photo_rating, current_user, db)
    return rating


@router.get("/{photo_id}", response_model=AvgRateResponse)
async def get_avg_rating(photo_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    photo = await repository_photos.get_photo(photo_id, db)
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    avg_rating = AvgRateResponse(photo_id=photo.id, avg_rating=photo.average_rating)
    return avg_rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=([Depends(allowed_edit_rating)]))
async def remove_rating(rating_id: int, db: Session = Depends(get_db)):
    rating = await repository_rating.remove_rating(rating_id, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo rating not found")
    return rating
