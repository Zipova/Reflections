from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Comment, User, Role
from src.schemas import CommentModel


async def add_comment(photo_id: int, body: CommentModel, current_user: User, db: Session):
    print(f'Photo: {photo_id}, comm: {body.comment}, user: {current_user.id}')
    comm = Comment(user_id=current_user.id, photo_id=photo_id, comment=body.comment)
    print(comm)
    db.add(comm)
    db.commit()
    db.refresh(comm)
    return comm


async def change_comment(photo_id: int, comment_id: int, body: CommentModel, current_user: User, db: Session):
    comm = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.photo_id == photo_id, Comment.user_id == current_user.id)).first()
    if comm:
        comm.comment = body.comment
        db.commit()
    return comm


async def delete_comment(photo_id: int, comment_id: int, current_user: User, db: Session):
    comm = db.query(Comment).filter(
        and_(Comment.id == comment_id, Comment.photo_id == photo_id, Comment.user_id == current_user.id)).first()
    if comm:
        db.delete(comm)
        db.commit()
    return comm
