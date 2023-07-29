import time
import calendar

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Photo, User, Role
from src.schemas import DescriptionUpdate


current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)


async def upload_photo(user_id: int, src_url: str, description: str, db: Session) -> Photo:
    new_photo = Photo(
        url=src_url, user_id=user_id, description=description
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return new_photo


async def get_all_photos(limit: int, offset: int, db: Session):
    photos = db.query(Photo).limit(limit).offset(offset).all()
    return photos


async def get_user_photos(limit: int, offset: int, user, db: Session):
    photos = db.query(Photo).filter(Photo.user_id == user.id).limit(limit).offset(offset).all()
    return photos


async def get_photo(photo_id: int, db: Session):
    return db.query(Photo).filter(Photo.id == photo_id).first()


async def remove_photo(photo_id: int, user: User, db: Session):
    if user.role == Role.admin:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
    else:
        photo = (
            db.query(Photo)
            .filter(and_(Photo.id == photo_id, Photo.user_id == user.id))
            .first()
        )
    if photo:
        db.delete(photo)
        db.commit()
    return photo


async def update_description(photo_id: int, body: DescriptionUpdate, user: User, db: Session):
    if user.role == Role.admin:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
    else:
        photo = (
            db.query(Photo)
            .filter(and_(Photo.id == photo_id, Photo.user_id == user.id))
            .first()
        )
    if photo:
        photo.description = body.description
        db.commit()
    return photo


async def search_photo_by_keyword(search_by: str, filter_by: str, db: Session):
    if filter_by == "creation_date":
        result = db.query(Photo).filter(Photo.description.like(search_by)).order_by(Photo.created_at).all()
    elif filter_by == "rating":
        result = db.query(Photo).filter(Photo.description.like(search_by)).order_by(Photo.average_rating).all()
    else:
        result = db.query(Photo).filter(Photo.description == search_by).all()
    return result
