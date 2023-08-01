from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Comment, User, Role, Photo
from src.schemas import CommentModel


async def add_comment(photo_id: int, body: CommentModel, current_user: User, db: Session):
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found")
    comm = Comment(user_id=current_user.id, photo_id=photo_id, comment=body.comment)
    print(comm)
    db.add(comm)
    db.commit()
    db.refresh(comm)
    return comm


async def change_comment(photo_id: int, comment_id: int, body: CommentModel, current_user: User, db: Session):
    comm = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.photo_id == photo_id, Comment.user_id == current_user.id)).first()
    if not comm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    comm.comment = body.comment
    db.commit()
    return comm


async def delete_comment(photo_id: int, comment_id: int, current_user: User, db: Session):
    comm = db.query(Comment).filter(
        and_(Comment.id == comment_id, Comment.photo_id == photo_id, Comment.user_id == current_user.id)).first()
    if not comm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(comm)
    db.commit()
