from sqlalchemy.orm import Session
from src.database.models import Tag


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).filter(Tag.name == name).first()


def create_tag(db: Session, name: str):
    tag = get_tag_by_name(db, name)
    if not tag:
        tag = Tag(name=name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    return tag
