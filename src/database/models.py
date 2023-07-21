import enum

from sqlalchemy import Column, Integer, String, Boolean, func, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Enum, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


photo_m2m_tag = Table(
    "photo_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("photo_id", Integer, ForeignKey("photos.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    created_at = Column('created_at', DateTime, default=func.now())
    photos = relationship('Photo', back_populates='user')
    comments = relationship('Comment', back_populates='user')


class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    description = Column(String(150), nullable=False)
    rating = Column(Float(), nullable=True)
    tags = relationship("Tag", secondary=photo_m2m_tag, backref="photos")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    author = relationship('User', back_populates='photos')
    comments = relationship('Comment', back_populates='photo')


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    photo_id = Column(ForeignKey("photos.id", ondelete="CASCADE"))
    comment = Column(String(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    photo = relationship('Photo', back_populates='comments')
    user = relationship('User', back_populates='comments')
