import time
import calendar
from typing import List


from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from src.database.models import Photo, User, Role, Tag
from src.schemas import DescriptionUpdate
from src.repository.tags import get_tag_by_name, create_tag


current_GMT = time.gmtime()
time_stamp = calendar.timegm(current_GMT)


async def upload_photo(user_id: int, src_url: str, tags: List[str], description: str, db: Session) -> Photo:

    new_photo = Photo(
        url=src_url, user_id=user_id, description=description)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    unique_tags = set() 
    for tag_name in tags[:5]:
        if tag_name not in unique_tags:
            tag = get_tag_by_name(db, tag_name)
            if not tag:
                tag = create_tag(db, tag_name)
            new_photo.tags.append(tag)
            unique_tags.add(tag_name)

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
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    return photo


async def get_user_photo(photo_id: int, user, db: Session):
    photo = db.query(Photo).filter(and_(Photo.user_id == user.id, Photo.id == photo_id)).first()
    return photo


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


async def search_photo_by_tag(tag: str, db: Session):
    photos = db.query(Photo).select_from(Photo).join(Photo.tags).filter(Tag.name == tag).all()
    return photos

