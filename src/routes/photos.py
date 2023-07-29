import calendar
import time
from fastapi import APIRouter, Depends, HTTPException, status, Form, Query


from typing import List

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import PhotoModel, PhotoDb, PhotoResponse, PhotoSearch
from src.repository import photos as repository_photos
from src.services.auth import auth_service
from src.services.roles import RolesChecker

current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)

router = APIRouter(prefix="/photos", tags=["photos"])

allowed_get_photo = RolesChecker([Role.admin, Role.moderator, Role.user])
allowed_post_photo = RolesChecker([Role.admin, Role.moderator, Role.user])
allowed_remove_photo = RolesChecker([Role.admin, Role.user])
allowed_update_photo = RolesChecker([Role.admin, Role.user])


@router.get("/", response_model=List[PhotoDb], dependencies=[Depends(allowed_get_photo)])
async def get_photos(
    limit: int = Query(10, le=100),
    offset: int = 0,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photos = await repository_photos.get_user_photos(limit, offset, current_user, db)
    return photos


@router.post("/upload", response_model=PhotoResponse, name="Upload photo", status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_post_photo)])
async def add_photo(
    description: str = Form(default=None),
    src_url: str = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photos.upload_photo(
        current_user.id, src_url, description, db
    )
    return {"photo": photo, "detail": "Photo has been upload successfully"}


@router.get("/{photo_id}", response_model=PhotoDb)
async def get_photo_by_id(
    photo_id: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    photo = await repository_photos.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


@router.delete(
    "/{photo_id}",
    response_model=PhotoDb,
    dependencies=[Depends(allowed_remove_photo)],
)
async def remove_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photos.remove_photo(photo_id, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


@router.put(
    "/{photo_id}",
    response_model=PhotoDb,
    dependencies=([Depends(allowed_update_photo)]),
)
async def update_photo_description(
    body: PhotoModel,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photos.update_description(photo_id, body, current_user, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo


@router.get("/search_keyword/", name="Search photos by keyword", response_model=List[PhotoDb]) #response_model=List[PhotoSearch]
async def search_photo_by_keyword(
    search_by: str,
    filter_by: str = Query(None, enum=["rating", "created_at"]),
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    if search_by:
        photo = await repository_photos.search_photo_by_keyword(search_by, filter_by, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    return photo
