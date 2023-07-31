import calendar
import time
from fastapi import APIRouter, Depends, HTTPException, status, Form, Query
from cloudinary import CloudinaryImage
from fastapi.responses import FileResponse

from typing import List

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas import PhotoModel, PhotoDb, PhotoResponse, PhotoSearch, CommentModel, CommentResponse, \
    PhotoResp
from src.repository import photos as repository_photos
from src.repository import comments as repository_comments
from src.services.auth import auth_service
from src.services.roles import RolesChecker
import qrcode
from io import BytesIO
import base64

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
    description: str = Form(),
    src_url: str = Form(),
    tags: List[str] = Form(default=[]),

    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    photo = await repository_photos.upload_photo(
        current_user.id, src_url, tags, description, db

    )
    return {"photo": photo, "detail": "Photo has been upload successfully"}


@router.get("/{photo_id}", response_model=PhotoResp)
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


@router.get("/{photo_id}/resize", response_class=FileResponse)
async def resize_photo(
    photo_id: int,
    width: int,
    height: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    public_url = CloudinaryImage(photo.url).build_url(
        width=width, height=height, crop="fill"
    )
    return FileResponse(public_url)


@router.get("/{photo_id}/crop", response_class=FileResponse)
async def crop_photo(
    photo_id: int,
    x: int,
    y: int,
    width: int,
    height: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    public_url = CloudinaryImage(photo.photo).build_url(
        width=width, height=height, crop="crop", gravity="auto",
        x=x, y=y
    )
    return FileResponse(public_url)


@router.get("/{photo_id}/rotate", response_class=FileResponse)
async def rotate_photo(
    photo_id: int,
    angle: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    public_url = CloudinaryImage(photo.photo).build_url(
        angle=angle
    )
    return FileResponse(public_url)


@router.post("/transform_and_create_link", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def transform_and_create_link(
    photo_id: int,
    width: int,
    height: int,
    current_user: User = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db),
):
    photo = await repository_photos.get_photo(photo_id, db)
    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
    public_url = CloudinaryImage(photo.photo).build_url(
        width=width, height=height, crop="fill"
    )

    photo.transformed_link = public_url

    qr_code_img = qrcode.make(public_url)
    qr_code_buffer = BytesIO()
    qr_code_img.save(qr_code_buffer)
    qr_code_buffer.seek(0)

    qr_code_base64 = base64.b64encode(qr_code_buffer.getvalue()).decode()
    photo.qr_code = qr_code_base64
    db.commit()
    return {
        "transformed_link": public_url,
        "qr_code": qr_code_base64,
    }
  
  
@router.post("/{photo_id}", response_model=CommentResponse) #додати комент до фотки
async def add_comment(photo_id: int, body: CommentModel,
                      current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comm = await repository_comments.add_comment(photo_id, body, current_user, db)
    return comm


@router.patch("/{photo_id}/{comment_id}", response_model=CommentResponse) #змінити комент
async def change_comment(photo_id: int, comment_id: int, body: CommentModel,
                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    comm = await repository_comments.change_comment(photo_id, comment_id, body, current_user, db)
    return comm


@router.delete("/{photo_id}/{comment_id}") #видалити комент
async def delete_comment(photo_id: int, comment_id: int, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    if current_user.role == Role.user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete comments!")
    await repository_comments.delete_comment(photo_id, comment_id, current_user, db)
    return 'Success'

