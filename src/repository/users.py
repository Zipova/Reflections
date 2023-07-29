from typing import Type

from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> Type[User] | None:
    """
           Returns user by his email.

           :param email: The email of user.
           :type email: str
           :param db: The database session.
           :type db: Session
           :return: The user with the specified email, or None if it does not exist.
           :rtype: Type[User] | None
           """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
           Creates a new specific user.

           :param body: The data for the user to create.
           :type body: UserModel
           :param db: The database session.
           :type db: Session
           :return: The newly created user.
           :rtype: User
           """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
            Updates a token for a specific user.

            :param user: The user to update the contact for.
            :type user: User
            :param token: The old token or None if it doesn't exist.
            :type token: str | None
            :param db: The database session.
            :type db: Session
            :return: Nothing.
            :rtype: None
            """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
            Confirms email of a specific user.

            :param email: The email of specific user.
            :type email: str
            :param db: The database session.
            :type db: Session
            :return: Nothing.
            :rtype: None
            """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
            Updates avatar for a specific user.

            :param email: The email of specific user.
            :type email: str
            :param url: The link of picture.
            :type url: str
            :param db: The database session.
            :type db: Session
            :return: Specific user with new avatar.
            :rtype: User
            """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
